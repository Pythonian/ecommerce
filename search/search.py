from search.models import SearchTerm
from catalog.models import Product
from django.db.models import Q
from stats import stats


STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
               'of', 'on', 'or', 'that', 'the', 'to', 'with']


def store(request, q):
    """ stores the search text in the database """
    # if search term is at least three chars long, store in db
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        # Get the ip address of the user conducting the search
        term.ip_address = request.META.get('REMOTE_ADDR')
        # Store a tracking id with each search
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated:
            term.user = request.user
        term.save()


def products(search_text):
    """ get products matching the search text """
    # Passes the search text through the function to get the search keywords as a list
    words = _prepare_words(search_text)
    # Create a list of all the products in the database
    products = Product.active.all()
    # Declare an empty dictionary to hold the result set
    results = {}
    results['products'] = []
    # Iterate through the keywords and filter
    for word in words:
        products = products.filter(
            Q(name__icontains=word) |
            Q(description__icontains=word) |
            Q(sku__iexact=word) |
            Q(brand__icontains=word) |
            Q(meta_description__icontains=word) |
            Q(meta_keywords__icontains=word)
        )
        # TODO: search for product price
        results['products'] = products
    return results


def _prepare_words(search_text):
    """ strip out common words, limit to 5 words """
    # Takes the search text and splits into list of individual word
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            # Strips out common words from the list
            words.remove(common)
    # Returns the first five words
    return words[0:5]

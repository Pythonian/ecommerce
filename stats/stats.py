import base64
import json
import os

from catalog.models import Product
from search.models import SearchTerm

from .models import ProductView

PRODUCTS_PER_ROW = 4

# Caution The urandom module is good for generating random bytes, which we convert to character strings in
# this example. However, the use of urandom is potentially very slow. In addition, urandom actually uses a random
# number generator provided by the operating system, which is /dev/urandom on Unix systems and
# CryptGenRandom on Windows. On some operating systems, the random number generator used may be a locked
# resource, which might result in the blocking of web requests.


def tracking_id(request):
    """ unique ID to determine what pages a customer has viewed """
    try:
        # Get the value of the session variable and return it if it exists
        return request.session['tracking_id']
    except KeyError:
        # If not, catch the error and assign random characters to the session variable.
        # Transform the Json into an integer array.
        request.session['tracking_id'] = json.dumps(
            list(base64.b64encode(os.urandom(36))))
        return request.session['tracking_id']


def recommended_from_search(request):
    """ get the common words from the stored searches """
    common_words = frequent_search_words(request)
    from search import search
    matching = []
    for word in common_words:
        results = search.products(word).get('products', [])
        for r in results:
            if len(matching) < PRODUCTS_PER_ROW and not r in matching:
                matching.append(r)
    return matching


def frequent_search_words(request):
    """ gets the three most common search words from the last 10 searches the current customer has entered """
    # get the ten most recent searches from the database.
    searches = SearchTerm.objects.filter(tracking_id=tracking_id(
        request)).values('q').order_by('-search_date')[0:10]
    # join all of the searches together into a single string.
    search_string = ' '.join([search['q'] for search in searches])
    # return the top three most common words in the searches
    return sort_words_by_frequency(search_string)[0:3]


def sort_words_by_frequency(some_string):
    """ takes a single string of space-delimited word and returns a list of words they contain from most to least frequent """
    # convert the string to a python list
    words = some_string.split()
    # assign a rank to each word based on frequency
    ranked_words = [[word, words.count(word)] for word in set(words)]
    # sort the words based on descending frequency
    sorted_words = sorted(ranked_words, key=lambda word: -word[1])
    # return the list of words, most frequent first
    return [p[0] for p in sorted_words]


def log_product_view(request, product):
    """ log the current customer as having viewed the given product instance """
    t_id = tracking_id(request)
    try:
        # Checks to see if the user has already viewed the particular product
        v = ProductView.objects.get(tracking_id=t_id, product=product)
        # Update the data associated with the product view
        v.save()
    except ProductView.DoesNotExist:
        # If user hasn't yet viewed a product, create and save a new ProductView model instance
        v = ProductView()
        v.product = product
        v.ip_address = request.META.get('REMOTE_ADDR')
        if not request.META.get('REMOTE_ADDR'):
            v.ip_address = '127.0.0.1'
        v.user = None
        v.tracking_id = t_id
        if request.user.is_authenticated:
            v.user = request.user
        v.save()


def recommended_from_views(request):
    """ get product recommendations based on products that the customer has viewed;
    gets list of tracking IDs of other customers who have viewed the products in the current customer's
    viewed products, and gets products that these other customers also viewed.

    """
    t_id = tracking_id(request)
    # get recently viewed products
    viewed = get_recently_viewed(request)
    # if there are previously viewed products, get other tracking ids that have
    # viewed those products also
    if viewed:
        productviews = ProductView.objects.filter(
            product__in=viewed).values('tracking_id')
        t_ids = [v['tracking_id'] for v in productviews]
        # if there are other tracking ids, get the products that those other customers viewed.
        if t_ids:
            all_viewed = Product.active.filter(
                productview__tracking_id__in=t_ids)
            # if there are other products, get them, excluding the products that the customer
            # has already viewed.
            if all_viewed:
                other_viewed = ProductView.objects.filter(
                    product__in=all_viewed).exclude(product__in=viewed)
                if other_viewed:
                    # Retrieve a list of products associated with this list of product views
                    return Product.active.filter(productview__in=other_viewed).distinct()


def get_recently_viewed(request):
    """ get settings.PRODUCTS_PER_ROW most recently viewed products for current customer """
    t_id = tracking_id(request)
    views = ProductView.objects.filter(tracking_id=t_id).values(
        'product_id').order_by('-date')[0:PRODUCTS_PER_ROW]
    product_ids = [v['product_id'] for v in views]
    return Product.active.filter(id__in=product_ids)

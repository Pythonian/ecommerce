from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import render

from . import search


def results(request):
    """ template for displaying paginated product results """
    # get current search phrase from the URL
    q = request.GET.get('q', '')
    # get current page number. Set to 1 if missing or invalid
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    # Retrieve the matching products
    matching = search.products(q).get('products', [])
    # generate the pagintor object
    paginator = Paginator(matching, 1)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
    # Store the search in the database
    search.store(request, q)

    page_title = 'Search Results for: ' + q

    template_name = 'search/results.html'
    context = {
        'q': q,
        'paginator': paginator,
        'results': results,
        'page_title': page_title,
        'results_count': matching.count(),
    }

    return render(request, template_name, context)

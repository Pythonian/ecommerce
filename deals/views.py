from django.shortcuts import render, get_object_or_404
from deals.models import Deal


def deals_list(request):
    """ List of active deals on the site """
    # Deal price, Published, Expiry
    deals = Deal.objects.all()[:4]
    page_title = 'Deals'

    template_name = 'deals/list.html'
    context = {
        'page_title': page_title,
        'deals': deals,
    }

    return render(request, template_name, context)

def detail(request, year, month, slug):

    deal = get_object_or_404(
        Deal, created__year=year, created__month=month,
        slug=slug)
    page_title = ''

    template_name = 'deals/detail.html'
    context = {
        'page_title': page_title,
        'deal': deal,
    }

    return render(request, template_name, context)
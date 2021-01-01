from django.shortcuts import get_object_or_404, render
from catalog.models import Category, Product, ProductReview
from catalog.forms import ProductAddToCartForm, ProductReviewForm
from django.template import RequestContext

from django.core import urlresolvers
from cart import cart
from django.http import HttpResponseRedirect, HttpResponse

from stats import stats

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import json

import tagging
from tagging.models import Tag, TaggedItem

from django.core.cache import cache
from ecomstore.settings import CACHE_TIMEOUT

PRODUCTS_PER_ROW = 4


def index(request):
    """ site home page """
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    page_title = 'Modern Musician | Musical Instruments and Sheet Music for Musicians'
    template_name = 'catalog/index.html'
    return render(request, template_name, locals())


def show_category(request, category_slug, template_name="catalog/category.html"):
    """ view for each individual category page """
    category_cache_key = request.path
    c = cache.get(category_cache_key)
    if not c:
        c = get_object_or_404(Category.active, slug=category_slug)
        cache.set(category_cache_key, c, CACHE_TIMEOUT)
    products = c.product_set.filter(is_active=True)
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description

    from django.db import connection
    queries = connection.queries

    template_name = 'catalog/category.html'
    context = {
        'category': category,
        'products': products,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description
    }

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_product(request, product_slug, template_name="catalog/product.html"):
    """ view for each product page """
    product_cache_key = request.path
    # try to get product from cache
    p = cache.get(product_cache_key)
    # if a cache miss, fall back on db query
    if not p:
        p = get_object_or_404(Product.active, slug=product_slug)
        # store item in cache for next time
        cache.set(product_cache_key, p, CACHE_TIMEOUT)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # evaluate the HTTP method, change as needed
    if request.method == 'POST':
        # create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if posted data is valid
        if form.is_valid():
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        # create the unbound form. Notice the request as a keyword argument
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set test cookie to make sure cookies are enabled
    request.session.set_test_cookie()
    # Logs a user who just viewed this product
    stats.log_product_view(request, p)
    # product review additions, CH 10
    product_reviews = ProductReview.approved.filter(
        product=p).order_by('-date')
    review_form = ProductReviewForm()
    context = {
        'categories': categories,
        'product': product,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'form': form,
        'product_reviews': product_reviews,
        'review_form': review_form
    }
    return render(request, template_name, context)


def tag_cloud(request, template_name="catalog/tag_cloud.html"):
    """ view containing a list of tags for active products, sized proportionately by relative
    frequency
    """
    product_tags = Tag.objects.cloud_for_model(Product, steps=9,
                                               distribution=tagging.utils.LOGARITHMIC,
                                               filters={'is_active': True})
    page_title = 'Product Tag Cloud'
    template_name = "catalog/tag_cloud.html"
    context = {
        'product_tags': product_tags,
        'page_title': page_title,
    }

    return render(request, template_name, context)


def tag(request, tag, template_name="catalog/tag.html"):
    """ view listing products that have been tagged with a given tag """
    products = TaggedItem.objects.get_by_model(Product.active, tag)
    page_title = 'Products tagged with ' + tag
    template_name = "catalog/tag.html"
    context = {
        'products': products,
        'page_title': page_title,
        'tag': tag,
    }

    return render(request, template_name, context)


@login_required
def add_review(request):
    """ AJAX view that takes a form POST from a user submitting a new product review;
    requires a valid product slug and args from an instance of ProductReviewForm;
    return a JSON response containing two variables: 'review', which contains
    the rendered template of the product review to update the product page,
    and 'success', a True/False value indicating if the save was successful.
    """
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        slug = request.POST.get('slug')
        product = Product.active.get(slug=slug)
        review.user = request.user
        review.product = product
        review.save()

        template = "catalog/product_review.html"
        html = render_to_string(template, {'review': review})
        response = json.dumps({'success': 'True', 'html': html})

    else:
        html = form.errors.as_ul()
        response = json.dumps({'success': 'False', 'html': html})
    return HttpResponse(response,
                        content_type='application/javascript; charset=utf-8')


@login_required
def add_tag(request):
    """ AJAX view that takes a form POST containing variables for a new product tag;
    requires a valid product slug and comma-delimited tag list; returns a JSON response
    containing two variables: 'success', indicating the status of save operation, and 'tag',
    which contains rendered HTML of all product pages for updating the product page.
    """
    tags = request.POST.get('tag', '')
    slug = request.POST.get('slug', '')
    if len(tags) > 2:
        p = Product.active.get(slug=slug)
        html = u''
        template = "catalog/tag_link.html"
        for tag in tags.split():
            tag.strip(',')
            Tag.objects.add_tag(p, tag)
        for tag in p.tags:
            html += render_to_string(template, {'tag': tag})
        response = simplejson.dumps({'success': 'True', 'html': html})
    else:
        response = simplejson.dumps({'success': 'False'})
    return HttpResponse(response,
                        content_type='application/javascript; charset=utf-8')


def product_list(request):
    """ a list of all product on the site. """
    products = Product.active.all()
    page_title = 'All Products'

    template_name = 'catalog/product_list.html'
    context = {
        'products': products,
        'page_title': page_title,
    }

    return render(request, template_name, context)


def variation_list(request, product_slug):
    """ a list of all variations for a product instance. """
    # Get the product
    product = get_object_or_404(Product, slug=product_slug)
    # Get all variations assoicated wih the product
    variations = Variation.objects.filter(product=product)
    # Returns only objects for a particular instance.
    formset = VariationFormSet(queryset=variations)

    if request.method == 'POST':
        formset = VariationFormSet(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_variation = form.save(commit=False)
                if new_variation.title:
                    product = get_object_or_404(Product, slug=product_slug)
                    new_variation.product = product
                    new_variation.save()
            messages.success(request, "Your inventory has been updated.")
            return redirect('product_list')
            # return HttpResponseRedirect(reverse('product_slug', kwargs={'product_slug': 'product_slug'}))

    template_name = 'catalog/variation_list.html'
    context = {
        'variations': variations,
        'formset': formset,
    }

    return render(request, template_name, context)

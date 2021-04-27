from django.shortcuts import render, reverse
from cart import cart


def show_cart(request):
    """ view function for the page displaying the customer shopping cart,
    and allows for the updating of quantities
    and removal product instances

    """
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            # checkout_url = checkout.get_checkout_url(request)
            # return HttpResponseRedirect(checkout_url)
            return reverse('checkout')
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)

    template = 'cart/cart.html'
    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'page_title': page_title
    }

    return render(request, template, context)

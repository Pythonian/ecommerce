from django.shortcuts import render, redirect
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem
from checkout import checkout
from cart import cart
from accounts import profile


def show_checkout(request):
    """ checkout form page to collect user shipping and billing information """
    if cart.is_empty(request):
        return redirect('show_cart')
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            # If the form is valid, pass along the request to the process checkout
            response = checkout.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                # If the order number was valid, redirect user to the receipt page.
                # Store the User's order number in the user's session for later use
                request.session['order_number'] = order_number
                return redirect('checkout_receipt')
        else:
            error_message = 'Correct the errors below'
    else:
        if request.user.is_authenticated:
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()
    page_title = 'Checkout'
    template_name = 'checkout/checkout.html'
    context = {
        'page_title': page_title,
        'form': form,
        'error_message': error_message
    }
    return render(request, template_name, context)


def receipt(request):
    """ page displayed with order information after an order has been placed successfully """

    # Retrieve the user's order number from its session
    order_number = request.session.get('order_number', '')
    if order_number:
        # If the number exists, retrieve the order information to be displayed
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        # Delete's the order number from the user's session since it's no longer needed
        del request.session['order_number']
    else:
        # Redirect a user with no order number to the cart page
        return redirect('show_cart')

    template_name = 'checkout/receipt.html'
    context = {
        'order_items': order_items
    }

    return render(request, template_name, context)

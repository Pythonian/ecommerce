from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect

from ecomstore.checkout.models import Order, OrderItem
from ecomstore.accounts.forms import UserProfileForm, RegistrationForm
from ecomstore.accounts import profile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user and user.is_active:
                login(request, user)
                return redirect('profile')
    else:
        form = RegistrationForm()
    page_title = 'User Registration'

    template_name = 'registration/register.html'
    context = {
        'form': form,
        'page_title': page_title,
    }

    return render(request, template_name, context)


@login_required
def my_account(request, template_name="registration/my_account.html"):
    """ page displaying customer account information, past order list and account options """
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    template_name = 'registration/profile.html'
    context = {
        'page_title': page_title,
        'orders': orders,
        'name': name
    }

    return render(request, template_name, context)


@login_required
def order_details(request, order_id, template_name="registration/order_details.html"):
    """ displays the details of a past customer order; order details can only be loaded by the same
    user to whom the order instance belongs.

    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    template_name = 'registration/order_details.html'
    context = {
        'order': order,
        'page_title': page_title,
        'order_items': order_items
    }

    return render(request, template_name, context)


@login_required
def order_info(request, template_name="registration/order_info.html"):
    """ page containing a form that allows a customer to edit their billing and shipping information that
    will be displayed in the order form next time they are logged in and go to check out """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        # form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
    else:
        user_profile = profile.retrieve(request)
        form = UserProfileForm(instance=user_profile)
        # form = UserProfileForm(instance=request.user.profile)
    page_title = 'Edit Order Information'

    template_name = 'registration/order_info.html'
    context = {
        # 'user_profile': user_profile,
        'form': form,
        'page_title': page_title
    }

    return render(request, template_name, context)

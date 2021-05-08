import http

from django.test import Client, TestCase
from django.urls import reverse

from cart import cart
from cart.models import CartItem
from catalog.models import Product

from .forms import CheckoutForm


class CheckoutTestCase(TestCase):
    """ tests checkout form page functionality """

    def setUp(self):
        self.client = Client()
        home_url = reverse('catalog_home')
        self.checkout_url = reverse('checkout')
        self.client.get(home_url)
        # need to create customer with a shopping cart first
        self.item = CartItem()
        product = Product.active.all()[0]
        self.item.product = product
        self.item.cart_id = self.client.session[cart.CART_ID_SESSION_KEY]
        self.item.quantity = 1
        self.item.save()

    def test_checkout_page_empty_cart(self):
        """ empty cart should be redirected to cart page """
        client = Client()
        cart_url = reverse('show_cart')
        response = client.get(self.checkout_url)
        self.assertRedirects(response, cart_url)

    def test_checkout_page(self):
        """ with at least one cart item, request for checkout page URL is successful """
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, "Checkout")
        url_entry = resolve(self.checkout_url)
        template_name = url_entry[2]['template_name']
        self.assertTemplateUsed(response, template_name)

    def test_submit_empty_form(self):
        """ empty order form raises 'required' error message for required order form fields """
        form = CheckoutForm()
        response = self.client.post(self.checkout_url, form.initial)
        for name, field in form.fields.iteritems():
            value = form.fields[name]
            if not value and form.fields[name].required:
                error_msg = form.fields[name].error_messages['required']
                self.assertFormError(response, "form", name, [error_msg])

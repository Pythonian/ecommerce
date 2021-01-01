from django.db import models
from catalog.models import Product


class CartItem(models.Model):
    """ model class containing information each Product instance in the customer's shopping cart """
    cart_id = models.CharField(max_length=50, db_index=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    @property
    def total(self):
        """
        Returns the extended price calculated from the product's price and the quantity of the cart item.
        """
        return self.quantity * self.product.price

    @property
    def name(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        """ called when a POST request comes in for a Product instance already in the shopping cart """
        # Adjust the cart quantity in case a User adds same product to the cart a second time.
        self.quantity = self.quantity + int(quantity)
        self.save()

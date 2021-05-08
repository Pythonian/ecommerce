from django.conf import settings
from django.db import models

from catalog.models import Product

User = settings.AUTH_USER_MODEL


class PageView(models.Model):
    """ model class for tracking the pages that a customer views """
    date = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=50, default='', db_index=True)

    class Meta:
        abstract = True


class ProductView(PageView):
    """ tracks product pages that customer views """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

import datetime

from django.db import models
from django.urls import reverse

from catalog.models import Product


class FeaturedDealManager(models.Manager):
    """ Manager class to return only those deals where each
    instance is featured, and is greater than the expiry date """

    def get_queryset(self):
        return super(FeaturedDealManager, self).get_queryset().filter(
            active=True).filter(featured=True).filter(
            expiry_date__gte=datetime.datetime.now())


class DealManager(models.Manager):
    def all(self):
        return


class Deal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    featured_deals = FeaturedDealManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('deal_detail', kwargs={
            'year': self.created.strftime("%Y"),
            'month': self.created.strftime("%m"),
            'slug': self.product.slug
        })

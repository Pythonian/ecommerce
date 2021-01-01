from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import tagging

from django.db.models.signals import post_save, post_delete
from ecomstore.caching.caching import cache_update, cache_evict


class ActiveCategoryManager(models.Manager):
    """ Manager class to return only those categories where
    each instance is active """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(models.Model):
    """ model class containing information about a category
    in the product catalog """
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Unique value for product page URL,created from name."
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        "Meta Keywords",
        max_length=255,
        help_text="Comma-delimited set of SEO keywords for meta tags."
    )
    meta_description = models.CharField(
        "Meta Description",
        max_length=255,
        help_text="Content for description meta tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveCategoryManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    @property
    def cache_key(self):
        return self.get_absolute_url()


class ActiveProductManager(models.Manager):
    """ Manager class to return only those products where
    each instance is active """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class FeaturedProductManager(models.Manager):
    """ Manager class to return only those products where
    each instance is featured """

    def all(self):
        return super().all().filter(is_active=True).filter(is_featured=True)


class Product(models.Model):
    """ model class containing information about a product;
    instances of this class are what the user
    adds to their shopping cart and can subsequently purchase

    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Unique value for product page URL, created from name."
    )
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    old_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        default=0.00
    )
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    meta_keywords = models.CharField(
        max_length=255,
        help_text="Comma-delimited set of SEO keywords for meta tag."
    )
    meta_description = models.CharField(
        max_length=255,
        help_text="Content for description meta tag."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    image = models.ImageField(upload_to='images/products/main')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    image_caption = models.CharField(max_length=200)

    objects = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_slug', kwargs={'product_slug': self.slug})

    @property
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def cross_sells(self):
        """ gets other Product instances that have been combined
        with the current instance in past orders. Includes the orders
        that have been placed by anonymous users that haven't registered
        """
        # The OrderItem model is dependent on the Product model,
        # so to avoid circular import, we import the models here.
        from ecomstore.checkout.models import Order, OrderItem
        # Look up past orders that includes the product we want to evaluate
        orders = Order.objects.filter(orderitem__product=self)
        # Look up other order items that were in the same orders
        # and exclude the product we're evaluating
        order_items = OrderItem.objects.filter(
            order__in=orders).exclude(product=self)
        # Get the associated products from the list of order items
        # and eliminate any duplicate
        products = Product.active.filter(orderitem__in=order_items).distinct()
        return products
    # users who purchased this product also bought....

    def cross_sells_user(self):
        """ gets other Product instances that have been ordered
        by other registered customers who also ordered the current
        instance. Uses all past orders of each registered customer
        and not just the order in which the current
        instance was purchased

        """
        from ecomstore.checkout.models import OrderItem
        from django.contrib.auth.models import User
        # Get the list of users who have purchased the current
        # product being evaluated
        users = User.objects.filter(order__orderitem__product=self)
        # Get a list of items those customers have ordered in the past
        # excluding the evaluated product
        items = OrderItem.objects.filter(
            order__user__in=users).exclude(product=self)
        # Get a list of the distinct products found listed in this
        # batch of order items
        products = Product.active.filter(orderitem__in=items).distinct()
        return products

    def cross_sells_hybrid(self):
        """ gets other Product instances that have been both been
        combined with the current instance in orders placed by
        unregistered customers, and all products that have ever
        been ordered by registered customers

        """
        from ecomstore.checkout.models import Order, OrderItem
        from django.db.models import Q
        # Get the list of orders that contains the evaluated product
        orders = Order.objects.filter(orderitem__product=self)
        # Get lists of users that have bought the evaluated product
        users = User.objects.filter(order__orderitem__product=self)
        # Filter out the order items based on the criteria excluding
        # the evaluated product
        items = OrderItem.objects.filter(
            Q(order__in=orders) | Q(order__user__in=users)
        ).exclude(product=self)
        # Get the list of active products
        products = Product.active.filter(orderitem__in=items).distinct()
        return products

    @property
    def cache_key(self):
        return self.get_absolute_url()


try:
    tagging.register(Product)
except tagging.AlreadyRegistered:
    pass


class ActiveProductReviewManager(models.Manager):
    """ Manager class to return only those product reviews
    where each instance is approved """

    def all(self):
        return super().all().filter(is_approved=True)


class ProductReview(models.Model):
    RATINGS = (
        (5, 5),
        (4, 4),
        (3, 3),
        (2, 2),
        (1, 1),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()

    objects = models.Manager()
    approved = ActiveProductReviewManager()


# attach signals to Product and Category model classes
# to update cache data on save and delete operations
post_save.connect(cache_update, sender=Product)
post_delete.connect(cache_evict, sender=Product)
post_save.connect(cache_update, sender=Category)
post_delete.connect(cache_evict, sender=Category)

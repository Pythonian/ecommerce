from django.contrib.auth.models import User
from django.db import models

from checkout.models import BaseOrderInfo


class UserProfile(BaseOrderInfo):
    """ stores customer order information used with the last order placed;
    can be attached to the checkout order form as a convenience to
    registered customers who have placed an order in the past.

    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

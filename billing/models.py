from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    data = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num = models.CharField(max_length=4)

    @property
    def display_number(self):
        return f'xxxxxxx-{self.num}'

    def __str__(self):
        return f'{self.user.username} - {self.display_number}'

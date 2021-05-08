from django.urls import path

from .views import add_card

urlpatterns = [
    path('add_card/', add_card, name='add_card'),
]

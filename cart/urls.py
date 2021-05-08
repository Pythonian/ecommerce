from django.urls import path

from .views import show_cart

urlpatterns = [
    path('', show_cart, name='show_cart'),
]

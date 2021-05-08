from django.urls import path

from .views import receipt, show_checkout

urlpatterns = [
    path('', show_checkout, name='checkout'),

    path('receipt/', receipt, name='receipt'),
]

from django.conf.urls import url
from checkout import views


urlpatterns = [
    url(r'^$',
        views.show_checkout,
        name='checkout'),

    url(r'^receipt/$',
        views.receipt,
        name='receipt'),
]

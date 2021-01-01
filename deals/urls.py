from django.conf.urls import url
from deals.views import deals_list, detail


urlpatterns = [
    url(r'^$', deals_list, name='deals_list'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<slug>[-\w]+)/$', detail, name='deal_detail'),
]
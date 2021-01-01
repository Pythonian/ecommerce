from django.conf.urls import url
from marketing.sitemaps import SITEMAPS
from marketing import views
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    url(r'^robots\.txt$',
        views.robots),
    url(r'^google_base\.xml$',
        views.google_base),
]

urlpatterns += [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS }),
]

from django.contrib.sitemaps.views import sitemap
from django.urls import path

from marketing.sitemaps import SITEMAPS

from .views import google_base, robots

urlpatterns = [
    path('robots.txt/', robots),
    path('google_base.xml/', google_base),
]

urlpatterns += [
    path('sitemap.xml/', sitemap, {'sitemaps': SITEMAPS}),
]

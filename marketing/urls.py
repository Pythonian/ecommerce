from django.urls import path
from marketing.sitemaps import SITEMAPS
from marketing import views
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('robots.txt/',
         views.robots),
    path('google_base.xml/',
         views.google_base),
]

urlpatterns += [
    path('sitemap.xml/', sitemap, {'sitemaps': SITEMAPS}),
]

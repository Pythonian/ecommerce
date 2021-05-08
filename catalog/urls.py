from django.urls import path

from .views import (add_review, add_tag, index, show_category, show_product,
                    tag, tag_cloud)

urlpatterns = [
    path('', index, name='catalog_home'),
    path('category/<slug:category_slug>/', show_category,
         name='category'),
    path('product/<slug:product_slug>/', show_product,
         name='catalog_product'),
    path('tag_cloud/', tag_cloud,
         name='tag_cloud'),
    path('tag/<slug:tag>/', tag, name='tag'),
    path('review/product/add/', add_review, name='add_product_review'),
    path('tag/product/add/', add_tag, name='add_tag'),
]

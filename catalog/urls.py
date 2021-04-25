from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='catalog_home'),
    path('category/<slug:category_slug>/', views.show_category,
         name='category'),
    path('product/<slug:product_slug>/', views.show_product,
         name='catalog_product'),
    path('tag_cloud/', views.tag_cloud,
         name='tag_cloud'),
    path('tag/<slug:tag>/', views.tag, name='tag'),
    path('review/product/add/', views.add_review, name='add_product_review'),
    path('tag/product/add/', views.add_tag, name='add_tag'),
]

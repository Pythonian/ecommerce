from django.contrib.auth import views as auth_views
from django.urls import path

from .views import my_account, order_details, order_info, register

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('my_account/', my_account, name='my_account'),
    path('order_info/', order_info, name='order_info'),
    path('order_details/(<int:order_id>)/', order_details,
         name='order_details'),
]

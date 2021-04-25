from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import (
    register, order_info, order_details, my_account)
from ecomstore import settings

urlpatterns = [
    # path('login/', auth_views.login,
    #      {'template_name': 'registration/login.html',
    #       'SSL': settings.ENABLE_SSL},
    #      name='login'),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('accounts/logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),
    path('register/', register,
         {'SSL': settings.ENABLE_SSL},
         name='register'),
    path('my_account/', my_account, name='my_account'),
    path('order_info/', order_info, name='order_info'),
    path('order_details/(<int:order_id>)/',
         order_details,
         name='order_details'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import register, profile, order_info, order_details
from ecomstore import settings

urlpatterns = [
	path('login/', auth_views.login,
	 	{'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL }, 
	 	name='login'),
	path('register/', register,
	    {'SSL': settings.ENABLE_SSL }, 
		name='register'),
	path('my_account/', my_account, name='my_account'),
	path('order_info/', order_info, name='order_info'),
	path('order_details/(<int:order_id>)/',
        order_details,
        name='order_details'),
]

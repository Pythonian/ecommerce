from django.urls import path
from search.views import results


urlpatterns = [
    path('results/', results, name='search_results'),
]

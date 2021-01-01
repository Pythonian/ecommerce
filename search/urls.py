from django.conf.urls import url
from search.views import results


urlpatterns = [
    url(r'^results/$',
        results,
        name='search_results'),
]

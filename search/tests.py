import http

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import html


class SearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        home_url = reverse('catalog_home')
        response = self.client.get(home_url)
        self.failUnless(response.status_code, http.HTTPStatus.OK)

    def test_html_escaped(self):
        """ search text displayed on results page is HTML-encoded """
        search_term = '<script>alert(xss)</script>'
        search_url = reverse('search_results')
        search_request = search_url + '?q=' + search_term
        response = self.client.get(search_request)
        self.failUnlessEqual(response.status_code, http.HTTPStatus.OK)
        escaped_term = html.escape(search_term)
        self.assertContains(response, escaped_term)

from django.test import TestCase
from django.urls import reverse, resolve

class TestUrls(TestCase):

    def setUp(self):
        self.get_countries_url = reverse('apis:countries-list')

    def test_get_countries(self):
        self.assertTrue(resolve(self.get_countries_url).func)

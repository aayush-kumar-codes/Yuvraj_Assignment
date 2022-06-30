from django.test import TestCase, Client
from django.urls import reverse
from location.models import Country, City


class TestViews(TestCase):
    def setUp(self) -> None:

        self.client = Client()
        self.location_url = reverse('apis:countries-list')

    def test_country_list(self):

        # test for getting country list
        self.country = Country.objects.create(
            country_code="IN", country_name="India")

        self.city = City.objects.create(
            country=self.country, city_name="Delhi")

        response = self.client.get(self.location_url)

        self.assertEqual(response.json(), [
                         {'id': 1, 'name': 'India', 'cities': [{'id': 1, 'name': 'Delhi'}]}])
        self.assertEqual(response.status_code, 200)

    def test_empty_country_list(self):
        
        # test for empty list
        response = self.client.get(self.location_url)
        self.assertEqual(response.json(), [])
        self.assertEqual(response.status_code, 200)

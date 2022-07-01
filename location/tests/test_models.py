from django.test import TestCase

from location.models import Country, City


class TestModels(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            country_code="IN", country_name="India")

        self.city = City.objects.create(
            country=self.country, city_name="Delhi")

    def test_country_created(self):
        # test case for adding country to model
        self.assertEqual(self.country.country_name, "India")
        self.assertEqual(self.country.country_code, "IN")

    def test_city_created(self):
        # test case for adding city to model
        self.assertEqual(self.city.country, self.country)
        self.assertEqual(self.city.city_name, "Delhi")
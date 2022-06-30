from django.test import TestCase
from django.contrib.auth.hashers import make_password

from users.models import NewUser
from location.models import Country, City


class TestModels(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            country_code="IN", country_name="India")

        self.city = City.objects.create(
            country=self.country, city_name="Delhi")

        self.new_user = NewUser.objects.create(email="test01@mailinator.com", user_name="test01", first_name="Test",
                                               last_name="Test", gender="male", age=22, country=self.country, city=self.city, password=make_password("Java@123"))

    def test_new_user_created(self):
        self.assertTrue(self.new_user.is_active)

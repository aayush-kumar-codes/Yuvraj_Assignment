from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from users.models import NewUser
from rest_framework.authtoken.models import Token
from location.models import Country, City


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.country = Country.objects.create(
            country_code="IN", country_name="India")

        self.city = City.objects.create(
            country=self.country, city_name="Delhi")

        self.new_user = NewUser.objects.create(email="test_user@meistery.net", user_name="test01", first_name="Test",
                                               last_name="Test", country=self.country, city=self.city, gender="male", age=22, password=make_password("trial_application"))
        self.credentials = {"email": "test_user@meistery.net",
                            "password": "trial_application"}

        self.token = Token.objects.create(user=self.new_user)
        self.login_url = reverse('apis:login')
        self.register_url = reverse('apis:register')
        self.logout_url = reverse('apis:logout')
        self.retrieve_url = reverse('apis:user_action', args=[1])
        self.update_url = reverse('apis:user_action', args=[1])

    def test_register_view(self):
        response = self.client.post(self.register_url, data={"email": "test_user2@meistery.net", "user_name": "test02", "first_name": "Test",
                                                             "last_name": "Test", "gender": "male", "country": 1, "city": 1, "age": 22, "password": "trial_application", "confirm_password": "trial_application"})
        
        self.assertTrue(response.json()['user_id'])
        self.assertEquals(response.status_code, 201)

    def test_login_view(self):

        response = self.client.post(
            self.login_url, self.credentials, follow=True)
        self.assertTrue(response.json()['user_id'])
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        
        # user logout api test  
        new_user = NewUser.objects.create(email="new_user@meistery.net", user_name="new_user", first_name="Test",
                                               last_name="Test", country=self.country, city=self.city, gender="male", age=22, password=make_password("trial_application"))
        token = Token.objects.create(user=new_user)
        response = self.client.get(self.logout_url, content_type="application/json",
            **{"HTTP_AUTHORIZATION": 'Token ' + token.key})

        self.assertEqual(response.json(), {"detail": "User Logged out successfully"})
        self.assertEqual(response.status_code, 200)

    def test_retrieve_view(self):

        # only authenticated users can retrieve data
        response = self.client.get(
            self.retrieve_url, content_type="application/json",
            **{"HTTP_AUTHORIZATION": 'Token ' + self.token.key},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'user_name': 'test01', 'first_name': 'Test', 'last_name': 'Test',
                         'email': 'test_user@meistery.net', 'gender': 'male', 'age': 22, 'country': 1, 'city': 1})

    def test_retrieve_view_not_authenticated(self):

        # only authenticated users can retrieve data
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_update_view(self):

        # test case for updating user data
        response = self.client.patch(self.update_url, data={"first_name": "Test01"}, content_type="application/json",
                                     **{"HTTP_AUTHORIZATION": 'Token ' + self.token.key},
                                     follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 1, 'user_name': 'test01', 'first_name': 'Test01', 'last_name': 'Test',
                         'email': 'test_user@meistery.net', 'gender': 'male', 'age': 22, 'country': 1, 'city': 1})

    def test_update_view_not_authorized(self):

        # Not authorized can't update data
        new_user = NewUser.objects.create(email="testuser@meistery.net", user_name="testuser", first_name="Test",
                                               last_name="Test", country=self.country, city=self.city, gender="male", age=22, password=make_password("trial_application"))
        token = Token.objects.create(user=new_user)
        response = self.client.patch(self.update_url, data={"first_name": "Test01"}, content_type="application/json",
                                     **{"HTTP_AUTHORIZATION": 'Token ' + token.key},
                                     follow=True)
        self.assertEqual(response.status_code, 403)
        

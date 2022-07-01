from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.models import Token

from sales.models import Sales
from users.models import NewUser


class TestViews(TestCase):
    def setUp(self) -> None:

        self.client = Client()

        # create two new users
        self.new_user = NewUser.objects.create(email="test_user@meistery.net", user_name="test01", first_name="Test",
                                               last_name="Test", gender="male", age=22, password=make_password("trial_application"))

        self.new_user_2 = NewUser.objects.create(email="test_user2@meistery.net", user_name="test_user2", first_name="Test",
                                                 last_name="Test", gender="male", age=22, password=make_password("trial_application"))

        # Add sales data, 2 for user 1 and 1 for user 2
        self.sales = Sales.objects.create(user=self.new_user, date=datetime(
            2020, 5, 17), product="Label", sales_number=20, revenue=10)
        self.sales = Sales.objects.create(user=self.new_user, date=datetime(
            2020, 5, 17), product="Paper", sales_number=32, revenue=8)
        self.sales = Sales.objects.create(user=self.new_user_2, date=datetime(
            2020, 5, 17), product="Paper", sales_number=32, revenue=8)

        # Generating Token for both users
        self.token = Token.objects.create(user=self.new_user)
        self.token_2 = Token.objects.create(user=self.new_user_2)

        # Accessing url patterns
        self.sales_list_url = reverse('apis:sales-list')
        self.sales_retrieve_url = reverse('apis:sales-detail', args=[1])
        self.sales_stats_url = reverse('apis:sales_statistics')

    def test_sales_list(self):

        # test for getting sales list
        response = self.client.get(self.sales_list_url, content_type="application/json",
                                   **{"HTTP_AUTHORIZATION": 'Token ' + self.token.key})

        self.assertEqual(response.json(), [{'id': 1, 'date': '2020-05-17', 'product': 'Label', 'sales_number': 20, 'revenue': 10.0, 'user': 1}, {
                         'id': 2, 'date': '2020-05-17', 'product': 'Paper', 'sales_number': 32, 'revenue': 8.0, 'user': 1}])

    def test_sales_list_not_authenticated(self):

        # test for getting sales list when user is not authenticated
        response = self.client.get(self.sales_list_url)

        self.assertEqual(response.json(), {
                         'detail': 'Authentication credentials were not provided.'})

    def test_add_new_sales_data(self):

        # test case for adding sales data
        response = self.client.post(self.sales_list_url, data={"date": "2022-05-17", "product": "Label", "sales_number": 20, "revenue": 10}, content_type="application/json",
                                    **{"HTTP_AUTHORIZATION": 'Token ' + self.token_2.key})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
                         'id': 4, 'date': '2022-05-17', 'product': 'Label', 'sales_number': 20, 'revenue': 10.0, 'user': 2})

    def test_add_new_sales_data_not_authenticated_user(self):

        # test case for adding sales data by not logged in user
        response = self.client.post(self.sales_list_url, data={
                                    "date": "2022-05-17", "product": "Label", "sales_number": 20, "revenue": 10})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
                         'detail': 'Authentication credentials were not provided.'})

    def test_retrieve_particular_record(self):
        # get a particular sales data by id
        response = self.client.get(self.sales_retrieve_url, content_type="application/json",
                                   **{"HTTP_AUTHORIZATION": 'Token ' + self.token.key})
        self.assertEqual(response.json(), {
                         'id': 1, 'date': '2020-05-17', 'product': 'Label', 'sales_number': 20, 'revenue': 10.0, 'user': 1})
        self.assertEqual(response.status_code, 200)

    def test_retrieve_particular_record_not_authorized_user(self):

        # test for getting sales list when user is not authenticated
        response = self.client.get(self.sales_retrieve_url, content_type="application/json",
                                   **{"HTTP_AUTHORIZATION": 'Token ' + self.token_2.key})
        self.assertEqual(response.json(), {
                         'detail': 'Sales data with id: 1, does not exists.'})
        self.assertEqual(response.status_code, 404)

    def test_sales_stats(self):

        # test casse for getting sales statistics
        response = self.client.get(self.sales_stats_url, content_type="application/json",
                                   **{"HTTP_AUTHORIZATION": 'Token ' + self.token.key})

        self.assertEqual(response.json(), {'average_sales_for_current_user': 0.34615384615384615, 'avergae_sale_all_user': 0.30952380952380953, 'highest_revenue_sale_for_current_user': {
                         'sale_id': 1, 'revenue': 10.0}, 'product_highest_revenue_for_current_user': {'product_name': 'Label', 'sales_number': 20}, 'product_highest_sales_for_current_user': {'product_name': 'Paper', 'sales_number': 32}})

        self.assertEqual(response.status_code, 200)

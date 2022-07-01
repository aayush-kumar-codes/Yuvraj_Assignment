from django.test import TestCase
from django.urls import reverse, resolve

from sales.api_v1.views import StatisticsView


class TestUrls(TestCase):

    def setUp(self):
        self.sales_list_url = reverse('apis:sales-list')
        self.sales_retrieve_url = reverse('apis:sales-detail', args=[1])
        self.sales_stats_url = reverse('apis:sales_statistics')

    def test_sales_list_url(self):
        # sales-list url can handle 'get' (list) and 'post' actions.
        self.assertTrue(resolve(self.sales_list_url).func)

    def test_sales_retrieve_url(self):
        # sales-detail url can handle 'get' (single record), 'put', 'update', 'delete' actions.
        self.assertTrue(resolve(self.sales_retrieve_url).func)

    def test_sales_statistics(self):
        # test statistics api url
        self.assertEqual(
            resolve(self.sales_stats_url).func.view_class, StatisticsView)

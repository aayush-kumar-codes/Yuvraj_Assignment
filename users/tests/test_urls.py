from django.test import TestCase
from django.urls import reverse, resolve

from users.api_v1.views import LoginView, RegisterView, UserActionView, LogoutView

class TestUrls(TestCase):

    def setUp(self):
        self.user_login_url = reverse('apis:login')
        self.user_register_url = reverse('apis:register')
        self.user_logout_url = reverse('apis:logout')
        self.user_retrieve_url = reverse('apis:user_action', args=[1])
        self.user_update_url = reverse('apis:user_action', args=[1])

    def test_login_url(self):
        self.assertEqual(resolve(self.user_login_url).func.view_class, LoginView)

    def test_register_url(self):
        self.assertEqual(resolve(self.user_register_url).func.view_class, RegisterView)

    def test_logout_url(self):
        self.assertEqual(resolve(self.user_logout_url).func.view_class, LogoutView)

    def test_user_retrieve(self):
        self.assertEqual(resolve(self.user_retrieve_url).func.view_class, UserActionView)

    def test_user_update(self):
        self.assertEqual(resolve(self.user_update_url).func.view_class, UserActionView)
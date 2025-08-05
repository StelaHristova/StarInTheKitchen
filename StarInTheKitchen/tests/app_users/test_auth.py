from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class RegisterPageTests(TestCase):
    def test_register_page_status_code(self):
        response = self.client.get(reverse('register-user'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login-user'))
        self.assertEqual(response.status_code, 200)


class LoginTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='test@example.com', password='pass1234')

    def test_valid_login(self):
        login = self.client.login(email='test@example.com', password='pass1234')
        self.assertTrue(login)
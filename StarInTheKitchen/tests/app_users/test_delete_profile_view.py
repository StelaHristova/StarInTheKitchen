from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from StarInTheKitchen.app_users.models import Profile


class ProfileDeleteTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='owner@example.com', password='pass1234')
        self.profile = self.user.profile

    def test_owner_can_delete_own_profile(self):
        self.client.login(email='owner@example.com', password='pass1234')
        response = self.client.post(reverse('delete-profile', args=[self.profile.pk]))

        self.assertRedirects(response, reverse('home-page'))

        self.assertFalse(Profile.objects.filter(pk=self.profile.pk).exists())

    def test_other_user_cannot_delete_profile(self):
        User = get_user_model()
        other_user = User.objects.create_user(email='new@example.com', password='pass1234')

        self.client.login(email='new@example.com', password='pass1234')
        response = self.client.post(reverse('delete-profile', args=[self.profile.pk]))

        self.assertNotEqual(response.status_code, 302)

        self.assertTrue(Profile.objects.filter(pk=self.profile.pk).exists())


from django.test import TestCase
from django.urls import reverse


class AsyncViewsTests(TestCase):
    def test_stats_view_returns_json(self):
        response = self.client.get(reverse('site-stats'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('recipes', response.json())
        self.assertIn('users', response.json())

    def test_latest_recipes_view_returns_json(self):
        response = self.client.get(reverse('latest-recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('latest_recipes', response.json())


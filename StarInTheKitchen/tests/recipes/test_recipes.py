from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from StarInTheKitchen.recipes.models import Recipe


class RecipeAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='test@example.com', password='pass1234')

    def test_my_recipes_requires_login(self):
        response = self.client.get(reverse('my-recipes'))
        self.assertEqual(response.status_code, 302)

    def test_my_recipes_view_logged_in(self):
        self.client.login(email='test@example.com', password='pass1234')
        response = self.client.get(reverse('my-recipes'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        recipe = Recipe.objects.create(
            title='Test',
            description='Desc',
            ingredients='Flour',
            instructions='Mix',
            prep_time=5,
            cook_time=10,
            servings=2,
            created_by=self.user,
            is_approved=True
        )
        response = self.client.get(reverse('recipe-detail', args=[recipe.pk]))
        self.assertEqual(response.status_code, 200)

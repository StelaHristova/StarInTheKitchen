from django import forms
from django.forms import Textarea
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'ingredients',
            'description',
            'instructions',
            'image',
            'prep_time',
            'cook_time',
            'servings',
            'meal_types',
            'seasons',
            'diets',
            'cooking_methods',
            'occasions',
        ]
        widgets = {
            'ingredients': Textarea(attrs={'rows': 4}),
            'description': Textarea(attrs={'rows': 3}),
            'instructions': Textarea(attrs={'rows': 6}),
        }
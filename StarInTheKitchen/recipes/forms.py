from django import forms
from django.forms import Textarea
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredients',
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
            'meal_types': forms.CheckboxSelectMultiple,
            'seasons': forms.CheckboxSelectMultiple,
            'diets': forms.CheckboxSelectMultiple,
            'cooking_methods': forms.CheckboxSelectMultiple,
            'occasions': forms.CheckboxSelectMultiple,
        }


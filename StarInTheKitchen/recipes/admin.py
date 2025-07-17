from django.contrib import admin
from .models import Recipe
from StarInTheKitchen.ingredients.models import Ingredient


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]


admin.site.register(Recipe, RecipeAdmin)
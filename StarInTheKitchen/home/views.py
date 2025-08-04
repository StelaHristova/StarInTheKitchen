from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import TemplateView

from StarInTheKitchen.recipes.models import Recipe
from StarInTheKitchen.categories.models import MealType, Season, Diet, CookingMethod, Occasion


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home/home-page.html'

    def get_top_recipe_image_for_category(self, category_qs, field_name):
        data = []
        for category in category_qs:
            recipes = Recipe.objects.filter(**{f"{field_name}__id": category.id}, is_approved=True).annotate(
                avg_score=Avg('reviews__rating')
            ).order_by('-avg_score', '-created_at')

            if recipes.exists() and recipes.first().image:
                data.append({
                    'category': category.name,
                    'recipe': recipes.first(),
                    'image_url': recipes.first().image.url,
                })

        return data

    # def get_template_names(self):
    #     if not self.request.user.is_authenticated:
    #         return ['index.html']
    #     return [self.template_name]
    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_recipes'] = Recipe.objects.filter(
            is_approved=True
        ).order_by('-created_at')[:6]

        context['meal_types'] = MealType.objects.all()
        context['seasons'] = Season.objects.all()
        context['diets'] = Diet.objects.all()
        context['methods'] = CookingMethod.objects.all()
        context['occasions'] = Occasion.objects.all()

        context['category_images'] = (
                self.get_top_recipe_image_for_category(MealType.objects.all(), 'meal_types') +
                self.get_top_recipe_image_for_category(Season.objects.all(), 'seasons') +
                self.get_top_recipe_image_for_category(Diet.objects.all(), 'diets') +
                self.get_top_recipe_image_for_category(CookingMethod.objects.all(), 'cooking_methods') +
                self.get_top_recipe_image_for_category(Occasion.objects.all(), 'occasions')
        )

        return context







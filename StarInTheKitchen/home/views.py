from django.shortcuts import render
from django.views.generic import TemplateView

from StarInTheKitchen.recipes.models import Recipe
from StarInTheKitchen.categories.models import MealType, Season, Diet, CookingMethod, Occasion


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home/home-page.html'

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
        return context
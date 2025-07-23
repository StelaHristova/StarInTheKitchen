from django.shortcuts import render
from django.views.generic import TemplateView

from StarInTheKitchen.recipes.models import Recipe


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_recipes'] = Recipe.objects.filter(
            is_approved=True
        ).order_by('-created_at')[:6]
        return context
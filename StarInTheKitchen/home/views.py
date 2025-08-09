from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.views.generic import TemplateView
from asgiref.sync import sync_to_async

from StarInTheKitchen.recipes.models import Recipe
from StarInTheKitchen.reviews.models import Review
from StarInTheKitchen.categories.models import MealType, Season, Diet, CookingMethod, Occasion


User = get_user_model()


class HomePageView(TemplateView, LoginRequiredMixin):
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


async def site_statistics_view(request):
    recipe_count = await Recipe.objects.acount()
    user_count = await User.objects.acount()
    review_count = await Review.objects.acount()

    return JsonResponse({
        'recipes': recipe_count,
        'users': user_count,
        'reviews': review_count,
    })


@sync_to_async
def get_latest_recipes():
    return list(
        Recipe.objects.filter(is_approved=True)
        .order_by('-created_at')[:5]
        .values('title', 'created_by__email', 'created_at')
    )


async def latest_recipes_view(request):
    recipes = await get_latest_recipes()

    for r in recipes:
        r['created_at'] = r['created_at'].strftime("%Y-%m-%d %H:%M")

    return JsonResponse({"latest_recipes": recipes})






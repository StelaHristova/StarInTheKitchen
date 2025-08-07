from django.urls import path
from StarInTheKitchen.api.views import RecipeListAPI, RecipeDetailAPI, ReviewListAPI

urlpatterns = [
    path('recipes/', RecipeListAPI.as_view(), name='api-recipes'),
    path('recipes/<int:pk>/', RecipeDetailAPI.as_view(), name='api-recipe-detail'),
    path('reviews/', ReviewListAPI.as_view(), name='api-reviews'),
]

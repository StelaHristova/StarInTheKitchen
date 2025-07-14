from django.urls import path
from .views import MealTypeListView

urlpatterns = [
    path('mealtypes/', MealTypeListView.as_view(), name='mealtype-list'),
]
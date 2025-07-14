from django.shortcuts import render
from django.views.generic import ListView

from StarInTheKitchen.categories.models import MealType


class MealTypeListView(ListView):
    model = MealType
    template_name = 'categories/mealtype_list.html'
    content_type = 'mealtypes'

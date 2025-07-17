from django.contrib import admin
from .models import MealType, Season, Diet, CookingMethod, Occasion

admin.site.register(MealType)
admin.site.register(Season)
admin.site.register(Diet)
admin.site.register(CookingMethod)
admin.site.register(Occasion)
from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'meal_types', 'created_by')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

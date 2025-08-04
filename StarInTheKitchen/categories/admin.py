from django.contrib import admin
from .models import MealType, Season, Diet, CookingMethod, Occasion, BaseCategory


# @admin.register(BaseCategory)
class BaseCategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'image')

    search_fields = ('name',)

    ordering = ('id',)

    list_filter = ('name',)


admin.site.register(MealType, BaseCategoryAdmin)
admin.site.register(Season, BaseCategoryAdmin)
admin.site.register(Diet, BaseCategoryAdmin)
admin.site.register(CookingMethod, BaseCategoryAdmin)
admin.site.register(Occasion, BaseCategoryAdmin)

from django.contrib import admin

from StarInTheKitchen.app_users.models import AppUser, Profile


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_superuser')
    ordering = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
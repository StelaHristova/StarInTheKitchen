from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('StarInTheKitchen.app_users.urls')),
    path('', include('StarInTheKitchen.home.urls')),
    path('categories/', include('StarInTheKitchen.categories.urls')),
    path('favourites/', include('StarInTheKitchen.favourites.urls')),
    path('recipes/', include('StarInTheKitchen.recipes.urls')),
    path('reviews/', include('StarInTheKitchen.reviews.urls')),
    path('api/', include('StarInTheKitchen.api.urls')),

]

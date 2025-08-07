from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('app_users.urls')),
    path('', include('home.urls')),
    path('categories/', include('categories.urls')),
    path('favourites/', include('favourites.urls')),
    path('recipes/', include('recipes.urls')),
    path('reviews/', include('reviews.urls')),
    path('api/', include('api.urls')),

]

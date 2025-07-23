from django.urls import path
from .views import toggle_favourite, my_favourites

urlpatterns = [
    path('toggle/<int:pk>/', toggle_favourite, name='toggle-favourite'),
    path('my/', my_favourites, name='my-favourites'),
]
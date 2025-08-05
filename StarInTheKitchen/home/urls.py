from django.urls import path
from .views import HomePageView, site_statistics_view, latest_recipes_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('stats/', site_statistics_view, name='site-stats'),
    path('latest/', latest_recipes_view, name='latest-recipes'),
]
from django.urls import path
from .views import submit_review

urlpatterns = [
    path('submit/<int:pk>/', submit_review, name='submit-review'),
]

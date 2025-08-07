from rest_framework import generics, permissions
from .serializers import RecipeSerializer, ReviewSerializer
from StarInTheKitchen.recipes.models import Recipe
from StarInTheKitchen.reviews.models import Review


class RecipeListAPI(generics.ListCreateAPIView):
    queryset = Recipe.objects.filter(is_approved=True)
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RecipeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewListAPI(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

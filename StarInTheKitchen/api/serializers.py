from rest_framework import serializers
from StarInTheKitchen.recipes.models import Recipe
from StarInTheKitchen.reviews.models import Review


class RecipeSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'ingredients',
            'instructions',
            'prep_time',
            'cook_time',
            'servings',
            'created_by',
            'created_at',
        ]
        read_only_fields = ['created_by', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

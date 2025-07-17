from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField

from StarInTheKitchen.categories.models import MealType, Season, Diet, CookingMethod, Occasion


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    ingredients = models.TextField(
        blank=True,
        null=True,
        help_text="Enter one ingredient per line, like:\n200g flour"
    )
    instructions = models.TextField()
    image = CloudinaryField(
        'image',
        blank=True,
        null=True
    )
    prep_time = models.PositiveIntegerField(
        help_text="In minutes"
    )
    cook_time = models.PositiveIntegerField(
        help_text="In minutes"
    )
    servings = models.PositiveIntegerField()
    is_approved = models.BooleanField(
        default=False
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    meal_types = models.ManyToManyField(
        MealType,
        blank=True
    )
    seasons = models.ManyToManyField(
        Season,
        blank=True
    )
    diets = models.ManyToManyField(
        Diet,
        blank=True
    )
    cooking_methods = models.ManyToManyField(
        CookingMethod,
        blank=True
    )
    occasions = models.ManyToManyField(
        Occasion,
        blank=True
    )

    def total_time(self):
        return self.prep_time + self.cook_time

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings
from StarInTheKitchen.recipes.models import Recipe


class Favourite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    added_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} → {self.recipe.title}"
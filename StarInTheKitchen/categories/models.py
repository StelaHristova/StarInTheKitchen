from cloudinary.models import CloudinaryField
from django.core import validators
from django.db import models


class BaseCategory(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        validators=[
            validators.MinLengthValidator(3, message="Category name needs to be at least 3 characters long.")
        ]
    )
    image = CloudinaryField('image', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class MealType(BaseCategory):
    pass


class Season(BaseCategory):
    pass


class Diet(BaseCategory):
    pass


class CookingMethod(BaseCategory):
    pass


class Occasion(BaseCategory):
    pass

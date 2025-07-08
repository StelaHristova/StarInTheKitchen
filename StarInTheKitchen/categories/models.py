from django.core import validators
from django.db import models


# Create your models here.
class MealType(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        validators=[
            validators.MinLengthValidator(3, message="Category name needs to be at least 3 characters long.")
        ]
    )

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        validators=[
            validators.MinLengthValidator(3, message="Category name needs to be at least 3 characters long.")
        ]
    )

    def __str__(self):
        return self.name


class Diet(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        validators=[
            validators.MinLengthValidator(3, message="Category name needs to be at least 3 characters long.")
        ]
    )

    def __str__(self):
        return self.name


class CookingMethod(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        validators=[
            validators.MinLengthValidator(3, message="Category name needs to be at least 3 characters long.")
        ]
    )

    def __str__(self):
        return self.name


class Occasion(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        validators=[
            validators.MinLengthValidator(3, message="Category name needs to be at least 3 characters long.")
        ]
    )

    def __str__(self):
        return self.name








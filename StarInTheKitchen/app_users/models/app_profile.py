from decouple import config
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from StarInTheKitchen.app_users.validators import first_name_validator, last_name_validator

AppUserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=AppUserModel,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
        blank=False,
        null=True,
        validators=[
            validators.MinLengthValidator(2, message="First name needs to be at least 2 characters long."),
            first_name_validator
        ],
    )

    last_name = models.CharField(
        max_length=30,
        blank=False,
        null=True,
        validators=[
            validators.MinLengthValidator(2, message="Last name needs to be at least 2 characters long."),
            last_name_validator
        ]
    )

    date_of_register = models.DateField(
        blank=True,
        null=True,
        auto_now_add=True,
    )

    profile_picture = CloudinaryField(
        resource_type='image',
        default=config('DEFAULT_PROFILE_IMAGE'),
        blank=True,
        null=True,
    )

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name

        return self.first_name or self.last_name or "Anonymous"

    models.JSONField
from django.core.exceptions import ValidationError


def first_name_validator(value):
    if not value.isalpha():
        raise ValidationError('First name needs to contain only alphabetic symbols.')

    return value


def last_name_validator(value):
    if not value.isalpha():
        raise ValidationError('Last name needs to contain only alphabetic symbols.')

    return value
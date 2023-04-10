from rest_framework.exceptions import ValidationError


def check_not_published(value):
    if value:
        raise ValidationError("Нельзя создать объявление, которое опубликовано ранее")

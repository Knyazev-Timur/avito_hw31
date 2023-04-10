from unicodedata import decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import check_brith_date, chek_email


class Location(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)
    lat = models.DecimalField("Латтитуда", max_digits=80, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField("Лонгитуда", max_digits=80, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class UserRoles(models.TextChoices):
    MEMBER = "member", "Пользователь"
    MODERATOR = "moderator", "Модератор"
    ADMIN = "admin", "Админ"


class User(AbstractUser):
    role = models.CharField(choices=UserRoles.choices, max_length=9, default=UserRoles.MEMBER)
    age = models.PositiveSmallIntegerField(null=True)
    location = models.ManyToManyField(Location)
    birth_date = models.DateField(validators=[check_brith_date], null=True)
    email = models.EmailField(unique=True, null=True, validators=[chek_email])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

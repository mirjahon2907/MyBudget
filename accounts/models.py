from django.db import models
from django.contrib.auth.models import AbstractUser


class Currency(models.TextChoices):
    UZS = 'UZS', 'UZS'
    USD = 'USD', 'USD'
    RUB = 'RUB', 'RUB'


class CustomUser(AbstractUser):

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UZS
    )


    def __str__(self):
        return self.username

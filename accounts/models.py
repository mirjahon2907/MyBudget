from django.db import models
from django.contrib.auth.models import AbstractUser


class Currency(models.TextChoices):
    UZS = 'UZS', 'UZS'
    USD = 'USD', 'USD'
    RUB = 'RUB', 'RUB'

class Gender(models.TextChoices):
    MALE = 'MALE', 'MALE'
    FEMALE = 'FEMALE', 'FEMALE'
    OTHER = "Other / Prefer not to say", "Other / Prefer not to say" 



class CustomUser(AbstractUser):

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UZS
    )

    phone_number = models.CharField(max_length=17)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    citizenship = models.CharField(max_length=50,null=True, blank=True)
    gender = models.CharField(choices=Gender.choices)
    passport = models.CharField(max_length=9,null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)




    def __str__(self):
        return self.username

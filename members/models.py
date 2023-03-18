from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Subscription(models.Model):
    user = models.OneToOneField(
        'CustomUser',
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )
    allergies = models.ManyToManyField(
        'recipes.Allergy',
        verbose_name='аллергии',
    )
    meals = models.ManyToManyField(
        'recipes.MealType',
        verbose_name='типы блюд',
    )

    def __str__(self):
        return self.user.username

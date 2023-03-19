from django.db import models
from django.contrib.auth.models import AbstractUser
from recipes.models import Allergy, MealType, MenuCategory 


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )

    menu_category = models.ForeignKey(
        MenuCategory,
        verbose_name='категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    duration = models.PositiveIntegerField(
        default=1,
        verbose_name='срок подписки (месяцев)',
    )
    allergies = models.ManyToManyField(
        Allergy,
        verbose_name='аллергии',
        blank=True,
    )
    meals = models.ManyToManyField(
        MealType,
        verbose_name='типы блюд',
        blank=True,
    )
    person_count = models.PositiveIntegerField(
        default=1,
        verbose_name='количество персон',
    )
    promo_code = models.CharField(
        max_length=20,
        verbose_name='промокод',
        blank=True,
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name='цена',
    )
    paid = models.BooleanField(
        default=False,
        verbose_name='оплачено',
    )

    def __str__(self):
        return self.user.username

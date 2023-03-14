from django.db import models


class Ingredient(models.Model):
    class AllergenGroup(models.IntegerChoices):
        SEA = 1, 'Рыба и морепродукты'
        MEAT = 2, 'Мясо'
        CEREAL = 3, 'Зерновые'
        BEES = 4, 'Продукты пчеловодства'
        NUTS_BEANS = 5, 'Орехи и бобовые'
        DAIRY = 6, 'Молочные продукты'
        __empty__ = ''

    name = models.CharField(
        'название',
        max_length=200,
        unique=True,
    )
    allergen_group = models.IntegerField(
        'аллергическая группа',
        choices=AllergenGroup.choices,
        blank=True,
        null=True,
    )
    calories = models.IntegerField(
        'Ккал на 100 г',
    )

    def __str__(self):
        return self.name

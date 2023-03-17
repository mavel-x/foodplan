from datetime import date

from django.db import models, transaction
from django.db.models import F, Sum, Value
from sortedm2m.fields import SortedManyToManyField


class AllergyGroup(models.IntegerChoices):
    SEA = 1, 'Рыба и морепродукты'
    MEAT = 2, 'Мясо'
    CEREAL = 3, 'Зерновые'
    BEES = 4, 'Продукты пчеловодства'
    NUTS_BEANS = 5, 'Орехи и бобовые'
    DAIRY = 6, 'Молочные продукты'
    __empty__ = ''


class Ingredient(models.Model):

    name = models.CharField(
        'название',
        max_length=200,
        unique=True,
    )
    allergy_group = models.IntegerField(
        'аллергическая группа',
        choices=AllergyGroup.choices,
        blank=True,
        null=True,
    )
    calories = models.IntegerField(
        'Ккал на 100 г',
    )
    liquid = models.BooleanField(
        'жидкий',
        default=False,
    )

    def __str__(self):
        return self.name


class Amount(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='amounts'
    )
    grams = models.IntegerField(
        'количество, г/мл'
    )

    def __str__(self):
        return f'{self.ingredient} {self.grams}'


class RecipeQuerySet(models.QuerySet):
    def with_calories(self):
        return self.annotate(
            calories=Sum(F('amounts__grams') * F('amounts__ingredient__calories') / Value(100)))

    def exclude_allergies(self, *allergies: AllergyGroup):
        return self.exclude(ingredients__allergy_group__in=allergies)


class Recipe(models.Model):
    class MealType(models.IntegerChoices):
        BREAKFAST = 1, 'завтрак'
        MAIN = 2, 'обед/ужин'
        DESSERT = 3, 'десерт'

    name = models.CharField(
        'название',
        max_length=200,
        unique=True,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='Amount',
        verbose_name='ингредиенты',
        related_name='recipes',
    )
    type = models.IntegerField(
        'тип',
        choices=MealType.choices
    )
    description = models.TextField(
        'описание',
        blank=True,
    )
    instructions = models.TextField(
        'инструкция по приготовлению',
        blank=True,
    )
    image = models.ImageField(
        'картинка',
        null=True,
        blank=True,
    )

    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return self.name

    def calories_individual(self):
        total = 0
        for amount in self.amounts.all():
            total += round(amount.grams * amount.ingredient.calories / 100)
        return total

    def allergies(self):
        allergies = set()
        for ingredient in self.ingredients.all():
            if ingredient.allergy_group:
                allergies.add(ingredient.get_allergy_group_display())
        return list(allergies)


class Weekday(models.IntegerChoices):
    MON = 1, 'Пн'
    TUE = 2, 'Вт'
    WED = 3, 'Ср'
    THU = 4, 'Чт'
    FRI = 5, 'Пт'
    SAT = 6, 'Сб'
    SUN = 7, 'Вс'


class DailyMenu(models.Model):
    meals = SortedManyToManyField(
        'Recipe',
    )

    def __str__(self):
        return ', '.join([meal.name for meal in self.meals.all()])


class WeekDayMenu(models.Model):
    day_menu = models.ForeignKey(
        'DailyMenu',
        on_delete=models.CASCADE,
        verbose_name='дневное меню',
        related_name='week_day_menus',
    )
    week = models.ForeignKey(
        'WeeklyMenu',
        on_delete=models.CASCADE,
        verbose_name='недельное меню',
        related_name='week_menus',
    )
    weekday = models.SmallIntegerField(
        'день недели',
        choices=Weekday.choices,
    )


class WeeklyMenu(models.Model):
    subscription = models.IntegerField(
        verbose_name='подписка'
    )
    year = models.SmallIntegerField(
        'год'
    )
    week = models.SmallIntegerField(
        'ISO номер недели',
    )
    daily_menus = models.ManyToManyField(
        'DailyMenu',
        verbose_name='дневные меню',
        through='WeekDayMenu',
    )

    def __str__(self):
        return f'{self.subscription} {self.year} {self.week}'

    @classmethod
    @transaction.atomic
    def build_random(cls, subscription_id, year, week):
        user_subscription = 666
        user_meals = [Recipe.MealType.MAIN, Recipe.MealType.MAIN, Recipe.MealType.BREAKFAST, Recipe.MealType.DESSERT]
        user_allergies = [AllergyGroup.BEES]

        allowed_recipes = (
            Recipe.objects
            .exclude_allergies(*user_allergies)
        )
        weekly_menu = cls.objects.create(
            subscription=user_subscription,
            year=year,
            week=week,
        )
        for day in Weekday:
            recipes = []
            for meal in sorted(user_meals):
                recipes.append(
                    allowed_recipes
                    .filter(type=meal)
                    .exclude(id__in=[recipe.id for recipe in recipes])
                    .order_by('?')
                    .first()
                )
            daily_menu = DailyMenu.objects.create()
            daily_menu.meals.add(*recipes)
            weekly_menu.daily_menus.add(
                daily_menu,
                through_defaults={
                    'weekday': day,
                }
            )
        return weekly_menu

    @classmethod
    def get_or_build_for_current_week(cls, subscription_id):
        today = date.today().isocalendar()
        try:
            return cls.objects.get(
                subscription=subscription_id,
                year=today.year,
                week=today.week)
        except cls.DoesNotExist:
            return cls.build_random(subscription_id, today.year, today.week)

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


class Allergy(models.Model):
    category = models.SmallIntegerField(
        'аллергическая группа',
        choices=AllergyGroup.choices,
    )

    def __str__(self):
        return self.get_category_display()


class MealGroup(models.IntegerChoices):
    BREAKFAST = 1, 'завтрак'
    MAIN = 2, 'обед/ужин'
    DESSERT = 3, 'десерт'


class MealType(models.Model):
    category = models.SmallIntegerField(
        'категория',
        choices=MealGroup.choices
    )
    label = models.CharField(
        'название',
        max_length=20,
    )

    def __str__(self):
        return f'{self.category}: {self.label}'


class MenuCategory(models.Model):
    title = models.CharField(
        verbose_name="Категория меню",
        max_length=200,
    )

    def __str__(self):
        return f'{self.title}'


class Ingredient(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        unique=True,
    )
    allergy_type = models.ForeignKey(
        'Allergy',
        verbose_name='аллергическая группа',
        on_delete=models.CASCADE,
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

    def exclude_allergies(self, *allergies: Allergy):
        return self.exclude(ingredients__allergy_type__in=allergies)


class Recipe(models.Model):
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
    category = models.ForeignKey(
        'MealType',
        verbose_name='категория',
        on_delete=models.CASCADE,
        null=True,
    )
    menu_category = models.ForeignKey(
        'MenuCategory',
        verbose_name='категория меню',
        on_delete=models.SET_NULL,
        null=True,
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
    subscription = models.ForeignKey(
        'members.Subscription',
        on_delete=models.CASCADE,
        verbose_name='подписка',
        related_name='weekly_menus'
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
        return f'{self.subscription}: {self.year}, week {self.week}'

    @classmethod
    @transaction.atomic
    def build_random(cls, user_subscription, year, week):
        user_meals = user_subscription.meals.order_by('category')
        user_allergies = user_subscription.allergies.all()
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
            for meal in user_meals:
                recipes.append(
                    allowed_recipes
                    .filter(category__category=meal.category)
                    .exclude(id__in=[recipe.id for recipe in recipes if recipe is not None])
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
    def get_or_build_for_current_week(cls, user_subscription):
        today = date.today().isocalendar()
        try:
            return cls.objects.get(
                subscription=user_subscription,
                year=today.year,
                week=today.week)
        except cls.DoesNotExist:
            return cls.build_random(user_subscription, today.year, today.week)

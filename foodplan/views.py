from django.shortcuts import render

from recipes.models import Recipe, MealGroup


def index(request):
    labels = [
        'Модный и полезный ужин',
        'Интересно, просто и супер вкусно',
        'Понятное всей семье, яркое на вкус',
        'Летнее удовольствие',
        'Который все пекут повторно',

    ]
    recipes = []
    all_recipes = Recipe.objects.all()
    meal_order = [MealGroup.MAIN, MealGroup.DESSERT, MealGroup.BREAKFAST]
    for meal in meal_order:
        recipes.extend(
            all_recipes.filter(category__pk=meal)[:2]
        )
    context = {'recipes_labels': zip(recipes, labels)}
    return render(request, 'index.html', context)

from django.shortcuts import render

from recipes.models import Recipe
from recipes.views import subscription_check


def index(request):
    has_subscription = False
    if request.user.is_authenticated:
        if subscription_check(request.user):
            has_subscription = True

    labels = [
        'Модный и полезный ужин',
        'Интересно, просто и супер вкусно',
        'Понятное всей семье, яркое на вкус',
        'Который все пекут повторно',
        'Летнее удовольствие',
    ]
    recipes = Recipe.objects.filter(pk__lte=5)
    context = {
        'recipes_labels': zip(recipes, labels),
        'has_subscription': has_subscription,
    }
    return render(request, 'index.html', context)

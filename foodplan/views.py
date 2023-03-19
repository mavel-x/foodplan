from django.shortcuts import render

from recipes.models import Recipe


def index(request):
    labels = [
        'Модный и полезный ужин',
        'Интересно, просто и супер вкусно',
        'Понятное всей семье, яркое на вкус',
        'Который все пекут повторно',
        'Летнее удовольствие',
    ]
    recipes = Recipe.objects.filter(pk__lte=5)
    context = {'recipes_labels': zip(recipes, labels)}
    return render(request, 'index.html', context)

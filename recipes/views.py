from django.shortcuts import render, get_object_or_404

from .models import Recipe


def recipe_card(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    amounts = recipe.amounts.prefetch_related('ingredient')
    context = {
        'recipe': recipe,
        'amounts': amounts,
    }
    return render(request, 'card.html', context)

from django.shortcuts import render, get_object_or_404

from .models import Recipe, AllergyGroup


def recipe_card(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    amounts = recipe.amounts.prefetch_related('ingredient')
    context = {
        'recipe': recipe,
        'amounts': amounts,
    }
    return render(request, 'card.html', context)


def daily_menu(request):
    # TODO
    # subscription = get_object_or_404(Subscription, pk=subscription_id)

    subscription_allergies = [AllergyGroup.BEES]
    subscription_meals = [Recipe.MealType.MAIN, Recipe.MealType.MAIN, Recipe.MealType.BREAKFAST, Recipe.MealType.DESSERT]

    allowed_recipes = (
        Recipe.objects
        .with_calories()
        .exclude_allergies(*subscription_allergies)
        .prefetch_related('amounts', 'ingredients')
    )
    recipes = []
    for meal in sorted(subscription_meals):
        recipes.append(
            allowed_recipes
            .filter(type=meal)
            .exclude(id__in=[recipe.id for recipe in recipes])
            .order_by('?')
            .first()
        )
    context = {'recipes': recipes}
    return render(request, 'daily_menu.html', context)

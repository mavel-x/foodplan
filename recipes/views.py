from django.shortcuts import render, get_object_or_404

from .models import Recipe, AllergyGroup, Weekday, WeeklyMenu


def recipe_card(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    amounts = recipe.amounts.prefetch_related('ingredient')
    context = {
        'recipe': recipe,
        'amounts': amounts,
    }
    return render(request, 'card.html', context)


def daily_menu(request, day):
    # TODO
    # subscription = get_object_or_404(Subscription, pk=subscription_id)
    subscription_id = 666

    weekly_menu = WeeklyMenu.get_or_build_for_current_week(subscription_id)
    recipes = weekly_menu.daily_menus.all()[day - 1].meals.all()

    context = {
        'recipes': recipes,
        'weekdays': Weekday,
        'cuurent_page': day,
    }
    return render(request, 'daily_menu.html', context)

from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse

from members.models import Subscription
from .models import Recipe, Weekday, WeeklyMenu


def subscription_check(user):
    return hasattr(user, 'subscription')


def recipe_card(request, recipe_id):
    if recipe_id > 5:
        if not request.user.is_authenticated:
            return redirect(f'{reverse("login")}?next={request.path}')
        elif not subscription_check(request.user):
            return redirect('profile')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    next_exists = Recipe.objects.filter(pk=recipe_id + 1).exists()
    amounts = recipe.amounts.prefetch_related('ingredient')
    context = {
        'recipe': recipe,
        'amounts': amounts,
        'previous_id': recipe_id - 1,
        'next_id': recipe_id + 1 if next_exists else None,
    }
    return render(request, 'card.html', context)


@login_required(login_url='login')
@user_passes_test(subscription_check, login_url='profile', redirect_field_name=None)
def daily_menu(request, day=None):
    if day is None:
        day = date.today().isoweekday()
        return redirect('daily-menu', day=day)
    elif day < 1 or day > 7:
        return redirect('daily-menu')

    subscription = Subscription.objects.get(user=request.user)
    weekly_menu = WeeklyMenu.get_or_build_for_current_week(subscription)
    recipes = weekly_menu.daily_menus.all()[day - 1].meals.all()

    context = {
        'recipes': recipes,
        'weekdays': Weekday,
        'current_page': day,
    }
    return render(request, 'daily_menu.html', context)

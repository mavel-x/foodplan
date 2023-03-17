from django.contrib import admin

from .models import Ingredient, Recipe, Amount, WeeklyMenu, DailyMenu, WeekDayMenu


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories', 'liquid', 'allergy_group']


class AmountInline(admin.TabularInline):
    model = Amount

    def calories_per_100_g(self, obj):
        return obj.ingredient.calories

    readonly_fields = ['calories_per_100_g']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [AmountInline]
    list_filter = ['type']

    def get_queryset(self, request):
        return super().get_queryset(request).with_calories()

    def calories(self, obj):
        return obj.calories

    list_display = ['name', 'type', 'calories', 'allergies']


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    pass


class WeekDayMenuInline(admin.TabularInline):
    model = WeekDayMenu


@admin.register(WeeklyMenu)
class WeeklyMenuAdmin(admin.ModelAdmin):
    inlines = [WeekDayMenuInline]

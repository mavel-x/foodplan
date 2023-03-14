from django.contrib import admin

from .models import Ingredient, Recipe, Amount


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

    def get_queryset(self, request):
        return super().get_queryset(request).with_calories()

    def calories(self, obj):
        return obj.calories

    list_display = ['name', 'type', 'calories']




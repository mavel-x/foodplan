from django.urls import path

from . import views

urlpatterns = [
    path('<int:recipe_id>/', views.recipe_card, name='recipe-card'),
]

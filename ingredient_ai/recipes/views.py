from django.shortcuts import render

from .selectors import (
    get_categories_with_ingredients,
    get_recipes_by_ingredients
)
from .services import generate_and_save_recipes


def get_ingredients(request):
    categories_with_ingredients = get_categories_with_ingredients()
    context = {'categories_with_ingredients': categories_with_ingredients}

    return render(request, 'recipes/index.html', context)


def get_recipes(request):
    if request.method == 'POST':
        selected_ingredients = request.POST.getlist('ingredient')
        generate_and_save_recipes(selected_ingredients)

        recipes = get_recipes_by_ingredients(selected_ingredients)
        context = {'recipes': recipes}

        return render(request, 'recipes/recipes.html', context)

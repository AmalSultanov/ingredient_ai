from django.core.cache import cache
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
        request.session['selected_ingredients'] = selected_ingredients
    else:
        selected_ingredients = request.session.get('selected_ingredients', [])

    if selected_ingredients:
        ingredients = '_'.join(selected_ingredients).lower()
        cache_key = f'recipes_with_{ingredients}_by_{request.user.id}'
        cached_recipes = cache.get(cache_key)

        if cached_recipes is None:
            generate_and_save_recipes(selected_ingredients)
            recipes = get_recipes_by_ingredients(selected_ingredients)

            cache.set(cache_key, recipes, timeout=None)
        else:
            recipes = cached_recipes

        context = {'recipes': recipes}

        return render(request, 'recipes/recipes.html', context)

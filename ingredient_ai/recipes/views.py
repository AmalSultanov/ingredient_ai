import logging

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .selectors import get_categories_with_ingredients
from .services import (
    get_selected_ingredients,
    set_selected_ingredients,
    get_recipes,
    get_cache_key
)

logger = logging.getLogger(__name__)


def get_ingredients_view(request):
    categories_with_ingredients = get_categories_with_ingredients()
    logger.info(f'Retrieved {len(categories_with_ingredients)} '
                f'categories with ingredients')

    return render(request, 'recipes/index.html',
                  {'categories_with_ingredients': categories_with_ingredients})


class RecipeView(View):
    template_name = 'recipes/recipes.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'Processing GET request for recipe view: {request.path}')
        selected_ingredients = get_selected_ingredients(request.session)
        logger.info(f'Selected ingredients for user '
                    f'{request.user.id}: {selected_ingredients}')
        recipes = get_recipes(user_id=request.user.id,
                              selected_ingredients=selected_ingredients)
        logger.info(f'Retrieved {recipes.count() if recipes else 0} '
                    f'recipes for selected ingredients')

        return render(request, self.template_name, {'recipes': recipes})

    def post(self, request, *args, **kwargs):
        logger.info(f'Processing POST request for: {request.path}')
        set_selected_ingredients(request)
        selected_ingredients = get_selected_ingredients(request.session)
        logger.info(f'Selected ingredients after '
                    f'form submission: {selected_ingredients}')
        recipes = get_recipes(user_id=request.user.id,
                              selected_ingredients=selected_ingredients)

        if recipes is None:
            cache_key = get_cache_key(request.user.id, selected_ingredients)

            return redirect(reverse('recipes:loading_page', args=[cache_key]))
        logger.info(f'Retrieved {recipes.count()} recipes to display')

        return render(request, self.template_name, {'recipes': recipes})


def loading_view(request, cache_key):
    return render(request, 'recipes/loading.html', {'cache_key': cache_key})


def check_recipes_ready(request, cache_key):
    recipes = cache.get(cache_key)

    return JsonResponse({'ready': recipes is not None})

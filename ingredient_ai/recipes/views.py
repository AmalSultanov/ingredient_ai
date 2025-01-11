from django.shortcuts import render

from .selectors import get_categories_with_ingredients


def get_ingredients(request):
    categories_with_ingredients = get_categories_with_ingredients()
    context = {'categories_with_ingredients': categories_with_ingredients}

    return render(request, 'recipes/index.html', context)

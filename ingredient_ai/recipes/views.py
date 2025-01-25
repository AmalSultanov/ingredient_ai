from django.shortcuts import render

from .selectors import get_categories_with_ingredients
from .services import get_recipes


def get_ingredients_view(request):
    categories_with_ingredients = get_categories_with_ingredients()
    context = {'categories_with_ingredients': categories_with_ingredients}

    return render(request, 'recipes/index.html', context)


def get_recipes_view(request):
    if request.method == 'POST':
        if request.session.get('selected_ingredients'):
            selected_ingredients = request.session.get('selected_ingredients')
        else:
            selected_ingredients = request.POST.getlist('ingredient')
            request.session['selected_ingredients'] = selected_ingredients
    else:
        selected_ingredients = request.session.get('selected_ingredients')

    recipes = get_recipes(user_id=request.user.id,
                          selected_ingredients=selected_ingredients)
    context = {'recipes': recipes}

    return render(request, 'recipes/recipes.html', context)

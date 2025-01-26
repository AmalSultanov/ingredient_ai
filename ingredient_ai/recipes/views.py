from django.shortcuts import render
from django.views import View

from .selectors import get_categories_with_ingredients
from .services import (
    get_selected_ingredients,
    set_selected_ingredients,
    get_recipes
)


def get_ingredients_view(request):
    categories_with_ingredients = get_categories_with_ingredients()
    context = {'categories_with_ingredients': categories_with_ingredients}

    return render(request, 'recipes/index.html', context)


class RecipeView(View):
    template_name = 'recipes/recipes.html'

    def get(self, request, *args, **kwargs):
        selected_ingredients = get_selected_ingredients(request.session)
        recipes = get_recipes(user_id=request.user.id,
                              selected_ingredients=selected_ingredients)

        return render(request, self.template_name, {'recipes': recipes})

    def post(self, request, *args, **kwargs):
        set_selected_ingredients(request)
        selected_ingredients = get_selected_ingredients(request.session)
        recipes = get_recipes(user_id=request.user.id,
                              selected_ingredients=selected_ingredients)
        return render(request, self.template_name, {'recipes': recipes})

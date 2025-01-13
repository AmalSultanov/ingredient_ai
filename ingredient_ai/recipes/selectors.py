from django.db.models import Q

from .models import IngredientCategoryModel, RecipeModel


def get_categories_with_ingredients():
    return IngredientCategoryModel.objects.prefetch_related(
        'ingredients'
    )


def get_recipes_by_ingredients(selected_ingredients):
    query = Q()

    for ingredient in selected_ingredients:
        query |= Q(ingredients__icontains=ingredient)

    return RecipeModel.objects.filter(query).distinct()

from django.db.models import Q, QuerySet

from .models import IngredientCategoryModel, RecipeModel


def get_categories_with_ingredients() -> QuerySet[IngredientCategoryModel]:
    return IngredientCategoryModel.objects.prefetch_related(
        'ingredients'
    )


def get_recipes_by_ingredients(
        selected_ingredients: list[str]
) -> QuerySet[RecipeModel]:
    if not selected_ingredients:
        return RecipeModel.objects.none()

    query = Q()

    for ingredient in selected_ingredients:
        query |= Q(ingredients__icontains=ingredient)

    return RecipeModel.objects.filter(query).distinct()


def get_recipes_by_ids(recipe_ids: set[int]) -> QuerySet[RecipeModel]:
    return RecipeModel.objects.filter(id__in=recipe_ids)

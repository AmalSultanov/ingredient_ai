from .models import IngredientCategoryModel


def get_categories_with_ingredients():
    return IngredientCategoryModel.objects.prefetch_related(
        'ingredients'
    )

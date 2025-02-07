import logging
from typing import Any

from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def validate_recipe_data(
        recipe_data: dict[str, Any],
        existing_recipes: set[str]
) -> None:
    required_fields = ['recipe_name', 'cooking_time', 'serving_size',
                       'description', 'ingredients', 'instructions']

    missing_fields = [field for field in required_fields if
                      field not in recipe_data]
    if missing_fields:
        logger.warning(f'Missing fields: {missing_fields}')
        raise ValidationError(
            {field: 'This field is required.' for field in missing_fields})

    if recipe_data['recipe_name'] in existing_recipes:
        raise ValidationError(
            {'name': 'Recipe with this name already exists.'})

    if (
            not isinstance(recipe_data['recipe_name'], str) or
            not recipe_data['recipe_name'].strip()
    ):
        raise ValidationError(
            {'recipe_name': 'Recipe name must be a non-empty string.'})

    if not isinstance(recipe_data['description'], str):
        raise ValidationError({'description': 'Description must be a string.'})

    if (
            not isinstance(recipe_data['cooking_time'], str) or
            len(recipe_data['cooking_time']) > 16
    ):
        raise ValidationError(
            {'cooking_time': 'Cooking time must be 16 characters or less.'})

    if (
            not isinstance(recipe_data['serving_size'], str) or
            len(recipe_data['serving_size']) > 16
    ):
        raise ValidationError(
            {'serving_size': 'Serving size must be 16 characters or less.'})

    if (
            not isinstance(recipe_data['ingredients'], list) or
            not all(
                isinstance(i, str) and
                i.strip() for i in recipe_data['ingredients'])
    ):
        raise ValidationError({
            'ingredients': 'Ingredients must be a list of non-empty strings.'})

    if (
            not isinstance(recipe_data['instructions'], list) or
            not all(
                isinstance(i, str) and
                i.strip() for i in recipe_data['instructions'])
    ):
        raise ValidationError({
            'instructions': 'Instructions must be a list of non-empty strings.'})

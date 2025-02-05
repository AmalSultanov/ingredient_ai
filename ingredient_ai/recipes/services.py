import json
import logging
from json import JSONDecodeError
from typing import Optional, Any

from django.contrib.sessions.backends.db import SessionStore
from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from ollama import chat

from .models import RecipeModel
from .selectors import get_recipes_by_ingredients
from .utils import get_prompt_file

logger = logging.getLogger(__name__)


def generate_and_save_recipes(selected_ingredients: list[str]) -> None:
    prompt = get_prompt_file()
    response = get_ai_response(prompt + ', '.join(selected_ingredients))

    save_generated_recipes(response)


def get_ai_response(prompt: str) -> str:
    response = chat(
        model='llama3.2:1b',
        messages=[{
            'role': 'user',
            'content': prompt,
        }]
    )
    logger.info('Received AI response')
    content = response['message']['content']

    return content


def save_generated_recipes(response: str) -> None:
    recipes_data = load_recipes_data(response)
    recipes = recipes_data.get('recipes', []) if recipes_data else None

    if not recipes:
        logger.info('No recipes to save')
        return

    existing_recipes = get_existing_recipe_names(recipes)
    new_recipes = prepare_new_recipes(recipes=recipes,
                                      existing_recipes=existing_recipes)

    if new_recipes:
        insert_new_recipes(new_recipes)
    else:
        logger.info('No new recipes to insert')


def load_recipes_data(
        response: str
) -> Optional[dict[str, list[dict[str, Any]]]]:
    try:
        logger.info('Loading generated recipes data')

        return json.loads(response)
    except JSONDecodeError as e:
        logger.error(f'Error decoding JSON response: {e}')

        return None


def get_existing_recipe_names(recipes: list[dict[str, Any]]) -> set[str]:
    recipe_names = [recipe['recipe_name'] for recipe in recipes]
    existing_recipes = set(
        RecipeModel.objects.filter(
            name__in=recipe_names
        ).values_list('name', flat=True)
    )

    return existing_recipes


def prepare_new_recipes(
        *,
        recipes: list[dict[str, Any]],
        existing_recipes: set[str]
) -> list[RecipeModel]:
    new_recipes = []
    logger.info(f'Saving {len(recipes)} recipe(s)')

    for recipe_data in recipes:
        name = recipe_data.get('recipe_name', '')
        if name in existing_recipes:
            logger.info(f'Skipping existing recipe: {name}')
            continue

        new_recipes.append(RecipeModel(
            name=name,
            cooking_time=recipe_data.get('cooking_time', ''),
            serving_size=recipe_data.get('serving_size', ''),
            description=recipe_data.get('description', ''),
            ingredients='\n'.join(recipe_data.get('ingredients', [])),
            instructions='\n'.join(recipe_data.get('instructions', []))
        ))

    return new_recipes


def insert_new_recipes(new_recipes: list[RecipeModel]) -> None:
    RecipeModel.objects.bulk_create(new_recipes, ignore_conflicts=True)
    logger.info(f'Inserted {len(new_recipes)} new recipe(s)')


def get_selected_ingredients(session: SessionStore) -> list[str]:
    return session.get('selected_ingredients', [])


def set_selected_ingredients(request: WSGIRequest) -> None:
    if 'selected_ingredients' not in request.session:
        selected_ingredients = request.POST.getlist('ingredient')
        request.session['selected_ingredients'] = selected_ingredients


def get_recipes(
        *,
        user_id: int | None,
        selected_ingredients: list[str]
) -> QuerySet[RecipeModel] | None:
    if not selected_ingredients:
        logger.warning('No ingredients selected, returning None')
        return None

    cache_key = get_cache_key(user_id, selected_ingredients)
    logger.info(f'Checking cache for key: {cache_key}')
    recipes = cache.get(cache_key) if cache_key else None

    if recipes is None:
        if not cache_key:
            recipes = get_recipes_for_unauthenticated(selected_ingredients)
            return recipes

        logger.info(f'Cache miss for key: {cache_key}. '
                    f'Generating and saving recipes')
        from .tasks import generate_and_save_recipes_task

        generate_and_save_recipes_task.delay(cache_key, selected_ingredients)

        return None
    return recipes


def get_cache_key(user_id: int, selected_ingredients: list[str]) -> str | None:
    if user_id:
        ingredients = '_'.join(selected_ingredients).lower()

        return f'recipes_with_{ingredients}_by_{user_id}'
    return None


def get_recipes_for_unauthenticated(
        selected_ingredients: list[str]
) -> QuerySet[RecipeModel]:
    logger.info('No user ID provided, generating recipes')
    generate_and_save_recipes(selected_ingredients)
    recipes = get_recipes_by_ingredients(selected_ingredients)

    return recipes


def cache_recipes(cache_key: str, recipes: QuerySet[RecipeModel]) -> None:
    cache.set(cache_key, recipes, timeout=None)
    logger.info(f'Saved recipes to cache with key: {cache_key}')

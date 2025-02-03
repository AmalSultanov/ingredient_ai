import json
import logging
from json import JSONDecodeError

from django.contrib.sessions.backends.db import SessionStore
from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
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
    try:
        logger.info('Saving generated recipes')
        recipes_data = json.loads(response)
    except JSONDecodeError as e:
        logger.error(f'Error decoding JSON response: {e}')

        return

    logger.info(f'Saving {len(recipes_data.get('recipes', []))} recipe(s)')
    for recipe_data in recipes_data.get('recipes', []):
        name = recipe_data.get('recipe_name', '')
        cooking_time = recipe_data.get('cooking_time', '')
        serving_size = recipe_data.get('serving_size', '')
        description = recipe_data.get('description', '')
        ingredients = '\n'.join(recipe_data.get('ingredients', []))
        instructions = '\n'.join(recipe_data.get('instructions', []))

        create_recipe(
            name=name,
            cooking_time=cooking_time,
            serving_size=serving_size,
            description=description,
            ingredients=ingredients,
            instructions=instructions
        )


def create_recipe(
        *,
        name: str,
        cooking_time: str,
        serving_size: str,
        description: str,
        ingredients: str,
        instructions: str
) -> RecipeModel:
    try:
        recipe = RecipeModel.objects.create(
            name=name,
            cooking_time=cooking_time,
            serving_size=serving_size,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
        )
        logger.info(f'Recipe created: {name}')

        return recipe
    except IntegrityError:
        logger.error(f'Recipe with name "{name}" already exists. Skipping')

        return None


def get_selected_ingredients(session: SessionStore) -> list[str]:
    return session.get('selected_ingredients', [])


def set_selected_ingredients(request: WSGIRequest) -> None:
    if 'selected_ingredients' not in request.session:
        selected_ingredients = request.POST.getlist('ingredient')
        request.session['selected_ingredients'] = selected_ingredients


def get_recipes(
        *,
        user_id: int,
        selected_ingredients: list[str]
) -> QuerySet[RecipeModel]:
    if not selected_ingredients:
        logger.warning('No ingredients selected, returning empty queryset')

        return RecipeModel.objects.none()

    if user_id is not None:
        ingredients = '_'.join(selected_ingredients).lower()
        cache_key = f'recipes_with_{ingredients}_by_{user_id}'
        logger.info(f'Checking cache for key: {cache_key}')
        recipes = cache.get(cache_key)

        if recipes is None:
            logger.info(f'Cache miss for key: {cache_key}. '
                        f'Generating and saving recipes')
            generate_and_save_recipes(selected_ingredients)
            recipes = get_recipes_by_ingredients(selected_ingredients)

            cache.set(cache_key, recipes, timeout=None)
        else:
            logger.info(f'Cache hit for key: {cache_key}')
    else:
        logger.info('No user ID provided, generating recipes')
        generate_and_save_recipes(selected_ingredients)
        recipes = get_recipes_by_ingredients(selected_ingredients)

    return recipes

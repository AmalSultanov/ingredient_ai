import json

from django.core.cache import cache
from ollama import chat

from .models import RecipeModel
from .selectors import get_recipes_by_ingredients
from .utils import get_prompt_file


def generate_and_save_recipes(selected_ingredients):
    prompt = get_prompt_file()
    response = get_ai_response(prompt + ', '.join(selected_ingredients))

    save_generated_recipes(response)


def get_ai_response(prompt):
    response = chat(
        model='llama3.2:1b',
        messages=[{
            'role': 'user',
            'content': prompt,
        }]
    )
    content = response['message']['content']

    return content


def save_generated_recipes(response):
    recipes_data = json.loads(response)

    for recipe_data in recipes_data.get('recipes', []):
        name = recipe_data.get('recipe_name', '')
        cooking_time = recipe_data.get('cooking_time', '')
        serving_size = recipe_data.get('serving_size', '')
        description = recipe_data.get('description', '')
        ingredients = '\n'.join(recipe_data.get('ingredients', []))
        instructions = '\n'.join(recipe_data.get('instructions', []))

        create_recipe(
            name,
            cooking_time,
            serving_size,
            description,
            ingredients,
            instructions
        )


def create_recipe(
        name,
        cooking_time,
        serving_size,
        description,
        ingredients,
        instructions
):
    recipe = RecipeModel.objects.create(
        name=name,
        cooking_time=cooking_time,
        serving_size=serving_size,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
    )

    return recipe


def get_recipes(user_id, selected_ingredients):
    ingredients = '_'.join(selected_ingredients).lower()
    cache_key = f'recipes_with_{ingredients}_by_{user_id}'
    recipes = cache.get(cache_key)

    if recipes is None:
        generate_and_save_recipes(selected_ingredients)
        recipes = get_recipes_by_ingredients(selected_ingredients)

        cache.set(cache_key, recipes, timeout=None)

    return recipes

import logging

from celery import shared_task

from .selectors import get_recipes_by_ingredients
from .services import generate_and_save_recipes, cache_recipes

logger = logging.getLogger(__name__)


@shared_task
def generate_and_save_recipes_task(
        cache_key: str | None,
        selected_ingredients: list[str]
) -> None:
    logger.info('Starting background task for recipe generation')

    generate_and_save_recipes(selected_ingredients)
    recipes = get_recipes_by_ingredients(selected_ingredients)
    cache_recipes(cache_key, recipes)

    logger.info('Finished recipe generation task')

import logging

from django.core.cache import caches

from ingredient_ai.recipes.selectors import get_recipes_by_ids

logger = logging.getLogger(__name__)
wishlist_cache = caches['wishlist']


def add_to_wishlist(user_id, recipe_id):
    key = f'wishlist_{user_id}'
    wishlist = wishlist_cache.get(key, set())
    logger.info(f'Adding recipe {recipe_id} to wishlist for user {user_id}')
    wishlist.add(recipe_id)
    wishlist_cache.set(key, wishlist)


def delete_from_wishlist(user_id, recipe_id):
    key = f'wishlist_{user_id}'
    wishlist = wishlist_cache.get(key, set())
    logger.info(f'Removing recipe {recipe_id} '
                f'from wishlist for user {user_id}')
    wishlist.discard(recipe_id)
    wishlist_cache.set(key, wishlist)


def get_wishlist(user_id):
    key = f'wishlist_{user_id}'
    wishlist_recipes_ids = wishlist_cache.get(key, set())
    wishlist_recipes = get_recipes_by_ids(wishlist_recipes_ids)

    if not wishlist_recipes:
        logger.info(f'No recipes found in wishlist for user {user_id}')
    else:
        logger.info(f'Fetched {len(wishlist_recipes)} recipes '
                    f'from wishlist for user {user_id}')

    return wishlist_recipes


def get_user_wishlist_ids(user_id):
    key = f'wishlist_{user_id}'
    wishlist_ids = wishlist_cache.get(key, set())

    if not wishlist_ids:
        logger.info(f'No wishlist IDs found for user {user_id}')
    else:
        logger.info(f'Fetched {len(wishlist_ids)} '
                    f'wishlist IDs for user {user_id}')

    return wishlist_ids

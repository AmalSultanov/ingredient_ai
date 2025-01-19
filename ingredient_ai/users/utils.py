from django.core.cache import caches

from ingredient_ai.recipes.selectors import get_recipes_by_ids

wishlist_cache = caches['wishlist']


def add_to_wishlist(user_id, recipe_id):
    key = f'wishlist_{user_id}'
    wishlist = wishlist_cache.get(key, set())
    wishlist.add(recipe_id)
    wishlist_cache.set(key, wishlist)


def delete_from_wishlist(user_id, recipe_id):
    key = f'wishlist_{user_id}'
    wishlist = wishlist_cache.get(key, set())
    wishlist.discard(recipe_id)
    wishlist_cache.set(key, wishlist)


def get_wishlist(user_id):
    key = f'wishlist_{user_id}'
    wishlist_recipes_ids = wishlist_cache.get(key, set())
    wishlist_recipes = get_recipes_by_ids(wishlist_recipes_ids)

    return wishlist_recipes


def get_user_wishlist_ids(user_id):
    key = f'wishlist_{user_id}'
    wishlist_recipes_ids = wishlist_cache.get(key, set())

    return wishlist_recipes_ids

from django.core.cache import caches

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

    return wishlist_cache.get(key, set())

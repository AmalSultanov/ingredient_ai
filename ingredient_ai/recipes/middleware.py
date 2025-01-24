from django.core.cache import cache
from django.urls import reverse


class ClearRecipeCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.recipes_url = reverse('recipes:recipes')

    def __call__(self, request):
        if not request.user.id:
            return self.get_response(request)

        user_cache_key = f'user_recipes_key_{request.user.id}'

        if request.method == 'POST' and request.path == self.recipes_url:
            selected_ingredients = request.POST.getlist('ingredient')
            ingredients = '_'.join(selected_ingredients).lower()
            cache_key = f'recipes_with_{ingredients}_by_{request.user.id}'

            cache.set(user_cache_key, cache_key)
        elif not (
                request.path == self.recipes_url or
                request.path.startswith('/users/add') or
                request.path.startswith('/users/delete')
        ) and user_cache_key in cache:
            cache.delete(cache.get(user_cache_key))
            cache.delete(user_cache_key)

        response = self.get_response(request)
        return response


class ClearIngredientsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'selected_ingredients' in request.session:
            if not (
                    request.path == reverse('recipes:recipes') or
                    request.path.startswith('/users/add') or
                    request.path.startswith('/users/delete')
            ):
                request.session.pop('selected_ingredients', None)

        response = self.get_response(request)
        return response

from django.core.cache import cache


class ClearRecipeCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cache_key = f'recipes_{request.user.id}'
        cache.delete(cache_key)

        response = self.get_response(request)
        return response

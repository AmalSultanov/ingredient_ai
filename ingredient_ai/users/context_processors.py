from .utils import get_wishlist


def wishlist_context(request):
    return {'user_wishlist': set(get_wishlist(request.user.id))}

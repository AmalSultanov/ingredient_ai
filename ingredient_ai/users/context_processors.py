from .services import get_user_wishlist_ids


def wishlist_context(request):
    return {'user_wishlist_ids': get_user_wishlist_ids(request.user.id)}

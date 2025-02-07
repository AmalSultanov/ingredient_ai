from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('registration/', views.RegistrationCreateView.as_view(),
         name='registration'),
    path('add-to-wishlist/<int:pk>', views.add_to_wishlist_view,
         name='add_to_wishlist'),
    path('delete-from-wishlist/<int:pk>', views.delete_from_wishlist_view,
         name='delete_from_wishlist'),
    path('wishlist/', views.get_wishlist_view, name='wishlist')
]

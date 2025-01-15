from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('wishlist/', views.get_wishlist_view, name='wishlist')
]

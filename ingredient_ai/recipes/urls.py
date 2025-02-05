from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.get_ingredients_view, name='ingredients'),
    path('recipes/', views.RecipeView.as_view(), name='recipes'),
    path('loading/<str:cache_key>/', views.loading_view, name='loading_page'),
    path('check-recipes/<str:cache_key>/', views.check_recipes_ready,
         name='check_recipes')
]

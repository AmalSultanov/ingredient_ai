from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.get_ingredients, name='ingredients'),
    path('generate-recipes/', views.generate_recipes, name='generate_recipes'),
    path('recipes/', views.get_recipes, name='recipes')
]

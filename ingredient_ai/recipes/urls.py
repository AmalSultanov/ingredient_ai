from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.get_ingredients, name='ingredients'),
    path('recipes/', views.get_recipes, name='recipes'),
]

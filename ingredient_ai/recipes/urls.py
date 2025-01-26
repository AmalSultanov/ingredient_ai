from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.get_ingredients_view, name='ingredients'),
    path('recipes/', views.RecipeView.as_view(), name='recipes')
]

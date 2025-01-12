from django.contrib import admin

from .models import IngredientCategoryModel, IngredientModel, RecipeModel


@admin.register(IngredientCategoryModel)
class IngredientCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    ordering = ['name']
    date_hierarchy = 'created_at'


@admin.register(IngredientModel)
class IngredientModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'category__name']
    ordering = ['category__name', 'name']


@admin.register(RecipeModel)
class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['cooking_time', 'serving_size', 'created_at']
    search_fields = ['name', 'cooking_time', 'serving_size', 'description',
                     'ingredients']

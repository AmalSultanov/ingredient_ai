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


@admin.register(RecipeModel)
class RecipeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_ingredients', 'created_at']
    list_filter = ['cooking_time', 'serving_size', 'created_at']
    search_fields = ['name', 'cooking_time', 'serving_size', 'description',
                     'ingredients__name']

    @staticmethod
    def get_ingredients(obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    get_ingredients.short_description = 'Ingredients'

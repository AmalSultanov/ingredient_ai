import unittest

from django.test import TestCase

from ..models import IngredientCategoryModel, RecipeModel
from ..selectors import (
    get_categories_with_ingredients,
    get_recipes_by_ingredients,
    get_recipes_by_ids
)


class SelectorsTestCase(TestCase):
    def setUp(self):
        self.category1 = IngredientCategoryModel.objects.create(name='Fruits')
        self.category2 = IngredientCategoryModel.objects.create(
            name='Vegetables')

        self.recipe1 = RecipeModel.objects.create(
            name='Apple Pie', ingredients='apple, sugar, flour')
        self.recipe2 = RecipeModel.objects.create(
            name='Salad', ingredients='lettuce, tomato, cucumber')
        self.recipe3 = RecipeModel.objects.create(
            name='Smoothie', ingredients='banana, milk, honey')

    def test_get_categories_with_ingredients(self):
        categories = get_categories_with_ingredients()
        self.assertEqual(categories.count(), 2)
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

    def test_get_categories_with_ingredients_empty(self):
        IngredientCategoryModel.objects.all().delete()
        categories = get_categories_with_ingredients()
        self.assertEqual(categories.count(), 0)

    def test_get_recipes_by_ingredients(self):
        selected_ingredients = ['apple', 'banana']
        recipes = get_recipes_by_ingredients(selected_ingredients)
        self.assertIn(self.recipe1, recipes)
        self.assertIn(self.recipe3, recipes)
        self.assertNotIn(self.recipe2, recipes)

    def test_get_recipes_by_ingredients_empty(self):
        recipes = get_recipes_by_ingredients([])
        self.assertEqual(recipes.count(), 0)

    def test_get_recipes_by_ingredients_case_insensitive(self):
        selected_ingredients = ['APPLE', 'BaNaNa']
        recipes = get_recipes_by_ingredients(selected_ingredients)
        self.assertIn(self.recipe1, recipes)
        self.assertIn(self.recipe3, recipes)

    def test_get_recipes_by_ids(self):
        recipe_ids = {self.recipe1.id, self.recipe3.id}
        recipes = get_recipes_by_ids(recipe_ids)
        self.assertIn(self.recipe1, recipes)
        self.assertIn(self.recipe3, recipes)
        self.assertNotIn(self.recipe2, recipes)

    def test_get_recipes_by_ids_empty(self):
        recipes = get_recipes_by_ids(set())
        self.assertEqual(recipes.count(), 0)

    def tearDown(self):
        IngredientCategoryModel.objects.all().delete()
        RecipeModel.objects.all().delete()


if __name__ == '__main__':
    unittest.main()

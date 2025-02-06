import unittest
from unittest.mock import patch

from django.test import TestCase

from ingredient_ai.recipes.tasks import generate_and_save_recipes_task


class TaskTestCase(TestCase):
    def setUp(self):
        self.cache_key = 'recipes_with_potato_by_1'
        self.selected_ingredients = ['tomato', 'cheese']

    @patch('ingredient_ai.recipes.tasks.generate_and_save_recipes')
    @patch('ingredient_ai.recipes.tasks.get_recipes_by_ingredients')
    @patch('ingredient_ai.recipes.tasks.cache_recipes')
    def test_generate_and_save_recipes_task(
            self, mock_cache_recipes, mock_get_recipes, mock_generate
    ):
        mock_get_recipes.return_value = [{'name': 'Tomato Cheese Pasta'}]
        generate_and_save_recipes_task(self.cache_key,
                                       self.selected_ingredients)

        mock_generate.assert_called_once_with(self.selected_ingredients)
        mock_get_recipes.assert_called_once_with(self.selected_ingredients)
        mock_cache_recipes.assert_called_once_with(
            self.cache_key, [{'name': 'Tomato Cheese Pasta'}]
        )


if __name__ == '__main__':
    unittest.main()

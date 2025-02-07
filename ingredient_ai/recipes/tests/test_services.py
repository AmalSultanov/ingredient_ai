import json
import unittest
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from ..models import RecipeModel
from ..services import (
    get_selected_ingredients,
    save_generated_recipes,
    generate_and_save_recipes,
    get_ai_response,
    load_recipes_data,
    get_existing_recipe_names,
    prepare_new_recipes,
    cache_recipes
)


class ServicesTestCase(TestCase):
    def setUp(self):
        self.session = self.client.session
        self.selected_ingredients = ['tomato', 'cheese']

    def test_get_selected_ingredients(self):
        self.session['selected_ingredients'] = ['tomato', 'cheese']
        self.session.save()
        self.assertEqual(get_selected_ingredients(self.session),
                         ['tomato', 'cheese'])

    def test_set_selected_ingredients(self):
        self.client.post(reverse('recipes:recipes'),
                         {'ingredient': ['tomato', 'cheese']})
        session = self.client.session
        session.save()
        self.assertEqual(session.get('selected_ingredients'),
                         ['tomato', 'cheese'])

    @patch('ingredient_ai.recipes.services.get_ai_response')
    @patch('ingredient_ai.recipes.services.save_generated_recipes')
    def test_generate_and_save_recipes(self, mock_save_recipes,
                                       mock_get_ai_response):
        mock_get_ai_response.return_value = '{"recipes": []}'
        generate_and_save_recipes(self.selected_ingredients)

        mock_get_ai_response.assert_called_once()
        mock_save_recipes.assert_called_once()

    @patch('ingredient_ai.recipes.services.chat')
    def test_get_ai_response(self, mock_chat):
        mock_chat.return_value = {"message": {"content": '{"recipes": []}'}}
        response = get_ai_response("test prompt")

        self.assertEqual(response, '{"recipes": []}')
        mock_chat.assert_called_once()

    def test_load_recipes_data_valid_json(self):
        valid_json = '{"recipes": [{"recipe_name": "Tomato Pasta"}]}'
        data = load_recipes_data(valid_json)

        self.assertIsInstance(data, dict)
        self.assertIn("recipes", data)

    def test_load_recipes_data_invalid_json(self):
        invalid_json = "{recipes: [invalid]}"
        data = load_recipes_data(invalid_json)

        self.assertIsNone(data)

    def test_get_existing_recipe_names(self):
        RecipeModel.objects.create(name='Tomato Pasta')
        existing_names = get_existing_recipe_names(
            [{'recipe_name': 'Tomato Pasta'}, {'recipe_name': "Cheese Pizza"}]
        )

        self.assertIn('Tomato Pasta', existing_names)
        self.assertNotIn('Cheese Pizza', existing_names)

    def test_prepare_new_recipes(self):
        recipes = [
            {'recipe_name': 'Tomato Pasta',
             'description': 'Delicious',
             'instructions': ['Step 1']},
            {'recipe_name': 'Cheese Pizza',
             'description': 'Yummy',
             'instructions': ['Bake cheese']}
        ]
        new_recipes = prepare_new_recipes(recipes=recipes)

        self.assertEqual(len(new_recipes), 2)
        self.assertEqual(new_recipes[0].name, 'Tomato Pasta')

    def test_cache_recipes(self):
        mock_recipes = [{'name': 'Tomato Soup'}]
        cache_recipes('recipes_with_potato_by_1', mock_recipes)
        cached_data = cache.get('recipes_with_potato_by_1')

        self.assertEqual(cached_data, mock_recipes)

    @patch('ingredient_ai.recipes.services.get_existing_recipe_names')
    @patch('ingredient_ai.recipes.services.insert_new_recipes')
    def test_save_generated_recipes(self, mock_insert_new_recipes,
                                    mock_get_existing):
        mock_response = json.dumps({
            'recipes': [
                {
                    'recipe_name': 'Tomato Pasta',
                    'cooking_time': '30-40 minutes',
                    'serving_size': '1-2 servings',
                    'description': 'Delicious tomato pasta',
                    'ingredients': ['Tomato', 'Pasta', 'Garlic'],
                    'instructions': ['Boil pasta', 'Make sauce',
                                     'Mix together']
                },
                {
                    'recipe_name': 'Cheese Pizza',
                    'cooking_time': '20 minutes',
                    'serving_size': '2-3 servings',
                    'description': 'Tasty cheese pizza',
                    'ingredients': ['Cheese', 'Flour', 'Tomato sauce'],
                    'instructions': ['Prepare dough', 'Add cheese', 'Bake']
                }
            ]
        })

        mock_get_existing.return_value = {'Tomato Pasta'}
        save_generated_recipes(mock_response)
        mock_insert_new_recipes.assert_called_once()
        inserted_recipes = mock_insert_new_recipes.call_args[0][0]

        self.assertEqual(len(inserted_recipes), 1)
        self.assertEqual(inserted_recipes[0].name, 'Cheese Pizza')

    def tearDown(self):
        self.client.session.flush()
        RecipeModel.objects.all().delete()
        cache.clear()


if __name__ == '__main__':
    unittest.main()

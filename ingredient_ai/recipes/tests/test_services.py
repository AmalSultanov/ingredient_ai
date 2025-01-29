import json
import unittest
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from ..models import RecipeModel
from ..services import get_selected_ingredients, save_generated_recipes


class ServicesTestCase(TestCase):
    def setUp(self):
        self.session = self.client.session

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
    def test_save_generated_recipes(self, mock_get_ai_response):
        mock_response = json.dumps({
            'recipes': [{
                'recipe_name': 'Tomato Pasta',
                'cooking_time': '30-40 minutes',
                'serving_size': '1-2 servings',
                'description': 'Delicious tomato pasta',
                'ingredients': ['Tomato', 'Pasta', 'Garlic'],
                'instructions': ['Boil pasta', 'Make sauce', 'Mix together']
            }]
        })
        mock_get_ai_response.return_value = mock_response
        save_generated_recipes(mock_response)
        self.assertTrue(
            RecipeModel.objects.filter(name='Tomato Pasta').exists()
        )

    def tearDown(self):
        self.client.session.flush()
        RecipeModel.objects.all().delete()


if __name__ == '__main__':
    unittest.main()

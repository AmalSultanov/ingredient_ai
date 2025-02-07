import unittest

from django.core.exceptions import ValidationError

from ..validators import validate_recipe_data


class ValidateRecipeDataTests(unittest.TestCase):
    def setUp(self):
        self.existing_recipes = {'Tomato Pasta'}
        self.valid_recipe = {
            'recipe_name': 'Cheese Pizza',
            'cooking_time': '20 minutes',
            'serving_size': '2-3 servings',
            'description': 'Delicious cheese pizza',
            'ingredients': ['Cheese', 'Flour', 'Tomato Sauce'],
            'instructions': ['Prepare dough', 'Add cheese', 'Bake']
        }

    def test_valid_recipe(self):
        try:
            validate_recipe_data(self.valid_recipe, self.existing_recipes)
        except ValidationError:
            self.fail(
                'validate_recipe_data() raised ValidationError unexpectedly!')

    def test_missing_fields(self):
        invalid_recipe = self.valid_recipe.copy()
        del invalid_recipe['recipe_name']

        with self.assertRaises(ValidationError) as context:
            validate_recipe_data(invalid_recipe, self.existing_recipes)
        self.assertIn('recipe_name', context.exception.message_dict)

    def test_duplicate_recipe_name(self):
        duplicate_recipe = self.valid_recipe.copy()
        duplicate_recipe['recipe_name'] = 'Tomato Pasta'

        with self.assertRaises(ValidationError) as context:
            validate_recipe_data(duplicate_recipe, self.existing_recipes)
        self.assertIn('name', context.exception.message_dict)

    def test_invalid_cooking_time_length(self):
        invalid_recipe = self.valid_recipe.copy()
        invalid_recipe['cooking_time'] = '12345678901234567'

        with self.assertRaises(ValidationError) as context:
            validate_recipe_data(invalid_recipe, self.existing_recipes)
        self.assertIn('cooking_time', context.exception.message_dict)

    def test_empty_ingredient(self):
        invalid_recipe = self.valid_recipe.copy()
        invalid_recipe['ingredients'] = ['']

        with self.assertRaises(ValidationError) as context:
            validate_recipe_data(invalid_recipe, self.existing_recipes)
        self.assertIn('ingredients', context.exception.message_dict)

    def test_empty_instructions(self):
        invalid_recipe = self.valid_recipe.copy()
        invalid_recipe['instructions'] = ['']

        with self.assertRaises(ValidationError) as context:
            validate_recipe_data(invalid_recipe, self.existing_recipes)
        self.assertIn('instructions', context.exception.message_dict)


if __name__ == '__main__':
    unittest.main()

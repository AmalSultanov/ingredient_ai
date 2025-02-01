import unittest

from django.test import TestCase
from django.urls import reverse

from ..models import RecipeModel


class ViewsTestCase(TestCase):
    def setUp(self):
        self.ingredients_url = reverse('recipes:ingredients')
        self.recipes_url = reverse('recipes:recipes')

    def test_get_ingredients_view(self):
        response = self.client.get(self.ingredients_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/index.html')

    def test_recipe_view_get(self):
        response = self.client.get(self.recipes_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')

    def test_recipe_view_post(self):
        response = self.client.post(self.recipes_url,
                                    {'ingredient': ['tomato', 'cheese']})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')
        self.assertTrue(RecipeModel.objects.exists())

    def tearDown(self):
        RecipeModel.objects.all().delete()


if __name__ == '__main__':
    unittest.main()

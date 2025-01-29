import unittest

from django.test import TestCase
from django.urls import reverse

from ..models import RecipeModel


class ViewsTestCase(TestCase):
    def test_get_ingredients_view(self):
        response = self.client.get(reverse('recipes:ingredients'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/index.html')

    def test_recipe_view_get(self):
        response = self.client.get(reverse('recipes:recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')

    def test_recipe_view_post(self):
        response = self.client.post(reverse('recipes:recipes'),
                                    {'ingredient': ['tomato', 'cheese']})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')
        self.assertTrue(RecipeModel.objects.exists())

    def tearDown(self):
        RecipeModel.objects.all().delete() if RecipeModel.objects.exists() \
            else None


if __name__ == '__main__':
    unittest.main()

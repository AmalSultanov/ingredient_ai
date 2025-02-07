import unittest

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from ..models import RecipeModel


class ViewsTestCase(TestCase):
    def setUp(self):
        self.cache_key = 'recipes_with_potato_by_1'
        self.ingredients_url = reverse('recipes:ingredients')
        self.recipes_url = reverse('recipes:recipes')
        self.loading_url = reverse('recipes:loading_page',
                                   args=[self.cache_key])
        self.check_recipes_url = reverse('recipes:check_recipes',
                                         args=[self.cache_key])

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
                                    {'name': 'Recipe 1',
                                     'ingredients': ['ingredient 1',
                                                     'ingredient 2']
                                     })

        self.assertEqual(response.status_code, 302)

    def test_loading_view(self):
        response = self.client.get(self.loading_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/loading.html')

    def test_check_recipes_not_ready(self):
        response = self.client.get(self.check_recipes_url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"ready": False})

    def test_check_recipes_ready(self):
        cache.set(self.cache_key, ['Recipe 1', 'Recipe 2'])
        response = self.client.get(self.check_recipes_url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"ready": True})

    def tearDown(self):
        RecipeModel.objects.all().delete()
        cache.clear()


if __name__ == '__main__':
    unittest.main()

import unittest

from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import get_ingredients_view, RecipeView


class UrlsTestCase(SimpleTestCase):
    def test_ingredients_url_resolves(self):
        url = reverse('recipes:ingredients')
        self.assertEqual(resolve(url).func, get_ingredients_view)

    def test_recipes_url_resolves(self):
        url = reverse('recipes:recipes')
        self.assertEqual(resolve(url).func.view_class, RecipeView)


if __name__ == '__main__':
    unittest.main()

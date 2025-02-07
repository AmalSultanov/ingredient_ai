import unittest

from django.core.cache import caches
from django.test import TestCase

from ingredient_ai.recipes.models import RecipeModel
from ..services import (
    add_to_wishlist,
    delete_from_wishlist,
    get_wishlist,
    get_user_wishlist_ids
)


class ServicesTestCase(TestCase):
    def setUp(self):
        self.cache = caches['wishlist']
        self.cache.clear()
        self.user_id = 1
        self.recipe_id = 101
        self.key = f'wishlist_{self.user_id}'

    def test_add_to_wishlist(self):
        add_to_wishlist(self.user_id, self.recipe_id)
        wishlist = self.cache.get(self.key, set())

        self.assertIn(self.recipe_id, wishlist)

    def test_delete_from_wishlist(self):
        self.cache.set(self.key, {self.recipe_id})
        delete_from_wishlist(self.user_id, self.recipe_id)
        wishlist = self.cache.get(self.key, set())

        self.assertNotIn(self.recipe_id, wishlist)

    def test_get_wishlist(self):
        recipe = RecipeModel.objects.create(name='Apple Pie',
                                            ingredients='apple, sugar, flour')
        self.cache.set(self.key, {recipe.id})
        wishlist = get_wishlist(self.user_id)

        self.assertIn(recipe, wishlist)

    def test_get_user_wishlist_ids(self):
        self.cache.set(self.key, {self.recipe_id})
        wishlist_ids = get_user_wishlist_ids(self.user_id)

        self.assertEqual(wishlist_ids, {self.recipe_id})

    def tearDown(self):
        self.cache.clear()


if __name__ == '__main__':
    unittest.main()

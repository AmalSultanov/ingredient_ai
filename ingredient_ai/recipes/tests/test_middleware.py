import unittest

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from ..models import RecipeModel


class ClearRecipeCacheMiddlewareTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test-user',
                                             password='password')
        self.recipes_url = reverse('recipes:recipes')

    def test_cache_set_on_post_request(self):
        self.client.login(username='test-user', password='password')
        response = self.client.post(self.recipes_url,
                                    {'ingredient': ['tomato', 'cheese']})
        cache_key = cache.get(f'user_recipes_key_{self.user.id}')

        self.assertIsNotNone(cache_key)
        self.assertTrue(cache_key.startswith('recipes_with_tomato_cheese_by_'))

    def test_cache_deletion_on_non_recipes_page(self):
        self.client.login(username='test-user', password='password')
        self.client.post(self.recipes_url,
                         {'ingredient': ['tomato', 'cheese']})
        user_cache_key = f'user_recipes_key_{self.user.id}'
        response = self.client.get(reverse('users:wishlist'))

        self.assertIsNone(cache.get(user_cache_key))

    def test_cache_not_set_for_anonymous_user(self):
        response = self.client.post(self.recipes_url,
                                    {'ingredient': ['tomato', 'cheese']})
        user_cache_key = f'user_recipes_key_None'

        self.assertIsNone(cache.get(user_cache_key))

    def tearDown(self):
        User.objects.first().delete()
        RecipeModel.objects.all().delete()
        cache.clear()


class ClearIngredientsMiddlewareTestCase(TestCase):
    def setUp(self):
        self.recipes_url = reverse('recipes:recipes')
        self.user = User.objects.create_user(username='test-user',
                                             password='password')

    def test_clear_selected_ingredients_in_session_on_non_recipes_page(self):
        session = self.client.session
        session['selected_ingredients'] = ['tomato', 'cheese']
        session.save()
        response = self.client.get(reverse('recipes:ingredients'))

        self.assertNotIn('selected_ingredients', self.client.session)

    def test_do_not_clear_selected_ingredients_on_recipes_page(self):
        self.client.force_login(self.user)
        session = self.client.session
        session['selected_ingredients'] = ['tomato', 'cheese']
        session.save()
        response = self.client.post(self.recipes_url,
                                    {'ingredient': ['tomato', 'cheese']})

        self.assertIn('selected_ingredients', self.client.session)
        self.assertEqual(self.client.session['selected_ingredients'],
                         ['tomato', 'cheese'])

    def tearDown(self):
        User.objects.first().delete()
        RecipeModel.objects.all().delete()
        self.client.session.flush()


if __name__ == '__main__':
    unittest.main()

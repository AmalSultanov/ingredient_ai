import unittest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, RequestFactory

from ..context_processors import wishlist_context


class ContextProcessorsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test-user',
                                             password='password')
        self.factory = RequestFactory()

    @patch('ingredient_ai.users.context_processors.get_user_wishlist_ids')
    def test_wishlist_context_with_items(self, mock_get_user_wishlist_ids):
        mock_get_user_wishlist_ids.return_value = {1, 2, 3}
        request = self.factory.get('users:wishlist')
        request.user = self.user
        context = wishlist_context(request)

        mock_get_user_wishlist_ids.assert_called_once_with(self.user.id)
        self.assertEqual(context, {'user_wishlist_ids': {1, 2, 3}})

    @patch('ingredient_ai.users.context_processors.get_user_wishlist_ids')
    def test_wishlist_context_with_no_items(self, mock_get_user_wishlist_ids):
        mock_get_user_wishlist_ids.return_value = set()
        request = self.factory.get('users:wishlist')
        request.user = self.user
        context = wishlist_context(request)

        mock_get_user_wishlist_ids.assert_called_once_with(self.user.id)
        self.assertEqual(context, {'user_wishlist_ids': set()})

    def tearDown(self):
        User.objects.first().delete()
        cache.clear()


if __name__ == '__main__':
    unittest.main()

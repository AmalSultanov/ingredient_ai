import unittest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from ..views import add_to_wishlist_view, delete_from_wishlist_view


class WishlistViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test-user',
                                             password='password')
        self.recipe_id = 101

    @patch('ingredient_ai.users.views.add_to_wishlist')
    def test_add_to_wishlist_view(self, mock_add_to_wishlist):
        request = self.factory.get('users/add-to-wishlist/101')
        request.user = self.user
        response = add_to_wishlist_view(request, self.recipe_id)

        mock_add_to_wishlist.assert_called_once_with(self.user.id,
                                                     self.recipe_id)
        self.assertEqual(response.status_code, 302)

    @patch('ingredient_ai.users.views.delete_from_wishlist')
    def test_delete_from_wishlist_view(self, mock_delete_from_wishlist):
        add_request = self.factory.get('users/add-to-wishlist/101')
        add_request.user = self.user
        add_to_wishlist_view(add_request, self.recipe_id)

        delete_request = self.factory.get('users/delete-from-wishlist/101')
        delete_request.user = self.user
        response = delete_from_wishlist_view(delete_request, self.recipe_id)

        mock_delete_from_wishlist.assert_called_once_with(self.user.id,
                                                          self.recipe_id)
        self.assertEqual(response.status_code, 302)

    def test_get_wishlist_view(self):
        response = self.client.get(reverse('users:wishlist'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/wishlist.html')

    def tearDown(self):
        User.objects.first().delete()


class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_registration_view(self):
        response = self.client.post(reverse('users:registration'),
                                    {'username': 'new-user',
                                     'email': 'qwe@gtbt.com',
                                     'password1': 'password123.password',
                                     'password2': 'password123.password'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='new-user').exists())

    def tearDown(self):
        User.objects.first().delete()


if __name__ == '__main__':
    unittest.main()

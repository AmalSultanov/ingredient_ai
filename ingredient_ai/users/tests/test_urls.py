import unittest

from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .. import views


class UrlsSimpleTestCase(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func.view_class, views.CustomLoginView)

    def test_registration_url_resolves(self):
        url = reverse('users:registration')
        self.assertEqual(resolve(url).func.view_class,
                         views.RegistrationCreateView)

    def test_add_to_wishlist_url_resolves(self):
        url = reverse('users:add_to_wishlist', args=[1])
        self.assertEqual(resolve(url).func, views.add_to_wishlist_view)

    def test_delete_from_wishlist_url_resolves(self):
        url = reverse('users:delete_from_wishlist', args=[1])
        self.assertEqual(resolve(url).func, views.delete_from_wishlist_view)

    def test_wishlist_url_resolves(self):
        url = reverse('users:wishlist')
        self.assertEqual(resolve(url).func, views.get_wishlist_view)


if __name__ == '__main__':
    unittest.main()

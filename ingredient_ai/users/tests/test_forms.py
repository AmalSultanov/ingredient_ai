import unittest

from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import RegistrationForm


class FormsTestCase(TestCase):
    def setUp(self):
        self.valid_form_data = {
            'username': 'test-user',
            'email': 'testuser@example.com',
            'password1': 'password123.password',
            'password2': 'password123.password',
        }
        self.invalid_email_data = {
            'username': 'test-user',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123',
        }
        self.password_mismatch_data = {
            'username': 'test-user',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'different_password',
        }

    def test_registration_form_valid(self):
        form = RegistrationForm(data=self.valid_form_data)

        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_missing_email(self):
        form_data = self.valid_form_data.copy()
        form_data['email'] = ''
        form = RegistrationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_form_invalid_password_mismatch(self):
        form = RegistrationForm(data=self.password_mismatch_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_registration_form_invalid_email(self):
        form = RegistrationForm(data=self.invalid_email_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_form_save_user(self):
        form = RegistrationForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'test-user')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password123.password'))

    def tearDown(self):
        User.objects.all().delete()


if __name__ == '__main__':
    unittest.main()

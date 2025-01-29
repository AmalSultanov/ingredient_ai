import os
import unittest
from unittest.mock import patch, mock_open

from django.test import TestCase

from ..utils import get_prompt_file, get_prompt_file_path


class UtilsTestCase(TestCase):
    # simulate reading a file without needing an actual file on disk
    @patch('builtins.open', new_callable=mock_open,
           read_data='Sample prompt.')
    # avoid dependency on the actual app configuration
    @patch('django.apps.apps.get_app_config')
    def test_get_prompt_file(self, mock_get_app_config, mock_open):
        mock_get_app_config.return_value.path = '/mock/app/path'
        prompt = get_prompt_file()
        mock_open.assert_called_once_with('/mock/app/path/prompts/prompt.txt',
                                          'r')

        self.assertEqual(prompt, 'Sample prompt.')

    @patch('django.apps.apps.get_app_config')
    def test_get_prompt_file_path(self, mock_get_app_config):
        mock_get_app_config.return_value.path = '/mock/app/path'
        prompt_file_path = get_prompt_file_path()
        expected_path = os.path.join('/mock/app/path', 'prompts', 'prompt.txt')

        self.assertEqual(prompt_file_path, expected_path)

    @patch('django.apps.apps.get_app_config')
    def test_get_prompt_file_path_with_custom_filename(
            self,
            mock_get_app_config
    ):
        mock_get_app_config.return_value.path = '/mock/app/path'
        prompt_file_path = get_prompt_file_path('custom_prompt.txt')
        expected_path = os.path.join('/mock/app/path', 'prompts',
                                     'custom_prompt.txt')

        self.assertEqual(prompt_file_path, expected_path)


if __name__ == '__main__':
    unittest.main()

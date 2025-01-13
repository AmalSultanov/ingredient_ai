import os

from django.apps import apps


def get_prompt_file_path(filename='prompt.txt'):
    app_config = apps.get_app_config('recipes')

    return os.path.join(app_config.path, 'prompts', filename)

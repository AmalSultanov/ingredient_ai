import os

from django.apps import apps


def get_prompt_file():
    prompt_file_path = get_prompt_file_path()

    with open(prompt_file_path, 'r') as file:
        prompt = file.read()

    return prompt


def get_prompt_file_path(filename='prompt.txt'):
    app_config = apps.get_app_config('recipes')

    return os.path.join(app_config.path, 'prompts', filename)

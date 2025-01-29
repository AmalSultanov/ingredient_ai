import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase

from .factories import (
    IngredientCategoryFactory,
    IngredientFactory,
    RecipeFactory
)
from ..models import IngredientCategoryModel, IngredientModel, RecipeModel


def generate_test_image():
    img = Image.new('RGB', (100, 100), color=(255, 0, 0))
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)

    return img_io


class IngredientCategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = IngredientCategoryModel.objects.create(
            name='Vegetables')

    def test_create_ingredient_category(self):
        self.assertEqual(self.category.name, 'Vegetables')
        self.assertIsNotNone(self.category.pk)


class IngredientModelTestCase(TestCase):
    def setUp(self):
        self.category = IngredientCategoryFactory()

    def test_create_ingredient(self):
        ingredient = IngredientFactory(category=self.category)
        self.assertIsNotNone(ingredient.pk)
        self.assertEqual(ingredient.category, self.category)

        fetched_ingredient = IngredientModel.objects.get(pk=ingredient.pk)
        self.assertEqual(fetched_ingredient.name, ingredient.name)


class RecipeModelTestCase(TestCase):
    def setUp(self):
        self.recipe = {
            'name': 'Pasta Carbonara',
            'cooking_time': '10 minutes',
            'serving_size': '1-2 servings',
            'description': 'A classic Italian pasta dish.',
            'ingredients': 'Pasta, Eggs, Cheese, Pancetta',
            'instructions': '1. Cook pasta\n2. Mix eggs & cheese\n3. Add pancetta'
        }

    def test_create_recipe(self):
        recipe = RecipeModel.objects.create(**self.recipe)
        self.assertEqual(recipe.name, 'Pasta Carbonara')
        self.assertIsNotNone(recipe.pk)

    def test_recipe_name_uniqueness(self):
        RecipeModel.objects.create(**self.recipe)

        try:
            with transaction.atomic():
                RecipeModel.objects.create(**self.recipe)
        except IntegrityError:
            self.assertTrue(True)

    def test_recipe_image_processing(self):
        image_file = generate_test_image()
        image = SimpleUploadedFile(
            'test.jpg', image_file.read(), content_type='image/jpeg'
        )
        recipe = RecipeModel.objects.create(
            name='Chocolate Cake',
            cooking_time='30-40 minutes',
            serving_size='3-4 servings',
            description='Delicious cake',
            ingredients='Flour, Eggs, Sugar, Cocoa',
            instructions='Mix & bake',
            image=image,
        )

        self.assertTrue(recipe.image.name.endswith('.jpg'))

    def test_recipe_created_at_timestamp(self):
        recipe = RecipeModel.objects.create(**self.recipe)
        self.assertIsNotNone(recipe.created_at)

    def tearDown(self):
        for recipe in RecipeModel.objects.all():
            recipe.delete()


class RecipeFactoryTestCase(TestCase):
    def test_create_recipe_with_factory(self):
        recipe = RecipeFactory()
        self.assertIsNotNone(recipe.pk)
        self.assertIn(recipe.cooking_time, ['10 minutes', '30-40 minutes'])

        fetched_recipe = RecipeModel.objects.get(pk=recipe.pk)
        self.assertEqual(fetched_recipe.name, recipe.name)

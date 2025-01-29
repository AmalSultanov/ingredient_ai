import io

import factory
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

from ..models import (
    IngredientCategoryModel,
    IngredientModel,
    RecipeModel
)

fake = Faker()


class IngredientCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IngredientCategoryModel

    name = factory.Faker('word')


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IngredientModel

    name = factory.Faker('word')
    category = factory.SubFactory(IngredientCategoryFactory)


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeModel

    name = factory.Faker('sentence', nb_words=3)
    cooking_time = factory.Faker('random_element',
                                 elements=['10 minutes', '30-40 minutes'])
    serving_size = factory.Faker('random_element',
                                 elements=['1-2 servings', '3-4 servings'])
    description = factory.Faker('paragraph')
    ingredients = factory.Faker('text')
    instructions = factory.Faker('text')

    @factory.post_generation
    def image(self, create, extracted, **kwargs):
        if extracted:
            self.image = extracted
        else:
            img = Image.new('RGB', (100, 100), color='blue')
            image_io = io.BytesIO()
            img.save(image_io, format='JPEG')
            image_io.seek(0)

            self.image = SimpleUploadedFile('test.jpg', image_io.read(),
                                            content_type='image/jpeg')

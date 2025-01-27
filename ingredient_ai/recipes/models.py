from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IngredientCategoryModel(TimeStampedModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ingredient category'
        verbose_name_plural = 'ingredient categories'


class IngredientModel(TimeStampedModel):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(
        IngredientCategoryModel,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'


class RecipeModel(TimeStampedModel):
    image = models.ImageField(upload_to='recipes', null=True, blank=True)
    name = models.CharField(max_length=64, unique=True)
    cooking_time = models.CharField(max_length=16)
    serving_size = models.CharField(max_length=16)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')

            image_name = f'{slugify(self.name)}.jpg'

            output = BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)

            self.image = ContentFile(output.read(), image_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

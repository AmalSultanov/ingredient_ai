from django.db import models


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
    image = models.ImageField(upload_to='recipes')
    name = models.CharField(max_length=64)
    cooking_time = models.PositiveSmallIntegerField()
    serving_size = models.PositiveSmallIntegerField()
    description = models.TextField()
    ingredients = models.ManyToManyField(
        IngredientModel,
        related_name='recipes'
    )
    instructions = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

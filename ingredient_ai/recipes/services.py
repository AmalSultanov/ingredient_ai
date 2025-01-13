from .models import RecipeModel


def create_recipe(name, cooking_time, serving_size, description, ingredients,
                  instructions):
    recipe = RecipeModel.objects.create(
        name=name,
        cooking_time=cooking_time,
        serving_size=serving_size,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
    )

    return recipe

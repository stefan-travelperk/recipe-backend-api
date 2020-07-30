from django.test import TestCase
from core import models


class ModelTests(TestCase):

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            name='Pizza',
            description='Put it in the oven'
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_ingredients_str(self):
        recipe = models.Recipe.objects.create(
            name='Pizza',
            description='Put it in the oven'
        )

        ingredient = models.Ingredient.objects.create(
            recipe=recipe,
            name='dough'
        )

        self.assertEqual(str(ingredient), ingredient.name)

from django.db import models


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients',
        null=True
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def add_ingredient(self, ingredients):
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=self, **ingredient)

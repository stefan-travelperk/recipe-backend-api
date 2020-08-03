from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        recipe = Recipe.objects.create(**validated_data)

        for ing in ingredients:
            Ingredient.objects.create(**ing, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')

        super(RecipeSerializer, self).update(instance, validated_data)

        Ingredient.objects.filter(recipe=instance).delete()

        for ing in ingredients:
            Ingredient.objects.create(**ing, recipe=instance)

        return instance

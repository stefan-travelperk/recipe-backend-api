from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(name='Pizza', description='Put it in the oven'):
    return Recipe.objects.create(name=name, description=description)


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


class RecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_by_id(self):
        recipe = sample_recipe()

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_with_ingredients(self):
        ing1 = 'tomato'
        ing2 = 'pepper'
        payload = {
            'name': 'lecso',
            'description': 'keverd ossze, es edd meg',
            'ingredients': [{'name': ing1}, {'name': ing2}]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key != 'ingredients':
                self.assertEqual(payload[key], getattr(recipe, key))

        self.assertTrue(recipe.ingredients.get(name=ing1))
        self.assertTrue(recipe.ingredients.get(name=ing2))

    def test_update_recipe(self):
        recipe = sample_recipe()

        payload = {
            "name": "Pizza",
            "description": "Put it in the microwave",
            "ingredients": [{"name": "cheese"}]
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')
        recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('name'), payload.get('name'))
        self.assertTrue(
            recipe.ingredients.get(
                name=payload.get('ingredients')[0]['name']
            )
        )
        self.assertEqual(recipe.description, payload['description'])

    def test_delete_recipe(self):
        recipe = sample_recipe()

        self.assertEqual(Recipe.objects.all().count(), 1)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.all().count(), 0)

    def test_filter_recipe(self):
        sample_recipe(name='filter name', description='ez egy leiras')
        sample_recipe(name='sima name', description='masik leiras')

        filt_text = 'filt'
        res = self.client.get(RECIPES_URL, {'name': filt_text})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.all().count(), 2)
        self.assertEqual(len(res.data), 1)
        self.assertIn(filt_text, res.data[0]['name'])

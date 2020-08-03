from rest_framework import viewsets,mixins

from core.models import Recipe

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        name_filter = self.request.query_params.get('name')

        if not name_filter:
            return super().get_queryset()

        self.queryset = self.queryset.filter(name__contains=name_filter)

        return self.queryset

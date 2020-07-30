from rest_framework import viewsets

from core.models import Recipe

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        name_filter = self.request.query_params.get('name')

        if name_filter:
            queryset = self.queryset
            queryset = queryset.filter(name__contains=name_filter)

            return queryset

        return self.queryset

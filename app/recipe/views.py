"""
Views for the recipe APIs.
"""
from tokenize import Token
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers


# There are various viewsets available

# The ModelViewSet is specifically set up to work directly with a model
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer

    # This queryset represents the objects that are available for this viewset
    # This is the way to tell the ModelViewSet which model to use
    queryset = Recipe.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # We override the get_query_method to make sure provided by ModelViewSet
    # to make sure the recipes are filtered down to the authenticated user
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # We override the method from ModelViewSet to specify another serializer
    # when the detail endpoint is called. We specifically will catch the 'list'
    # from the reverse(url), which is the action variable in ModelViewSet,
    # meaning, most of our functionalities will use the Detail serializer
    # In all situations EXCEPT OF THE LISTING we will want to use the Detail.
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    # This method will be called by django_rest_framework after serializer
    # has been already validated (get_serializer_class). It is an override
    def perform_create(self, serializer):
        """Create a new recipe."""

        # By default, perform_create in ViewSetModel does not use any attributes,
        # with below statement, we modify the behaviour so it creates it for the user
        serializer.save(user=self.request.user)


class TagViewSet(mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

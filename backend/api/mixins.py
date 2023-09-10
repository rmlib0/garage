from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    """Basic ViewSet class for create, list, destroy."""


class ListRetrieveViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
):
    """Basic ViewSet class for list, retrieve."""

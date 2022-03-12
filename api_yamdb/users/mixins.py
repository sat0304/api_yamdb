from rest_framework.viewsets import GenericViewSet, mixins


class RetrieveUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    pass

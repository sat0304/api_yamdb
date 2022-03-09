from rest_framework.viewsets import GenericViewSet, mixins


class SignupViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


class TokenViewSet(mixins.UpdateModelMixin, GenericViewSet):
    pass
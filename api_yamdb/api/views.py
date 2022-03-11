from django.core.exceptions import PermissionDenied
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import OwnerOrReadOnly
from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

class ModelMixinSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass

class CreateListDeleteMixinSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDeleteMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDeleteMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Только Администратор может создавать произведение!')
        serializer.save()

    def perform_update(self, serializer):
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(TitleViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer, *args, **kwargs):
        instance = Title.objects.get(pk=self.kwargs.get('pk'))
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

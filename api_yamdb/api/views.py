from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import GenreFilter, TitleFilter
from .mixins import CreateListDeleteMixinSet
from .permissions import AdminOrSuperuser, IsAuthenticatedOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet(CreateListDeleteMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('=name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'create':
            return (AdminOrSuperuser(),)
        if self.action == 'destroy':
            return (AdminOrSuperuser(),)
        return super().get_permissions()


class GenreViewSet(CreateListDeleteMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    filter_class = GenreFilter

    def get_permissions(self):
        if self.action == 'create':
            return (AdminOrSuperuser(),)
        if self.action == 'destroy':
            return (AdminOrSuperuser(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter
    filterset_fields = (
        'category__slug',
        'genre__slug',
        'name',
        'year')

    def get_serializer_class(self):
        if self.action in (
            'list',
            'retrieve'
        ):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_permissions(self):
        if self.action in (
            'create',
            'destroy',
            'partial_update'
        ):
            return (AdminOrSuperuser(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(rating=None)

from ast import Not
from unicodedata import category
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
            
    def perform_create(self, serializer):
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Только Администратор может создавать категории!')
        serializer.save()

    def perform_destroy(self, serializer, *args, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    """@action(detail=False, methods=['delete'])
    def group_names(self, request, pk=None):
        slug = get_object_or_404(Genre, id=self.kwargs.get('id'))
        return Response([slug])"""

    def perform_create(self, serializer):
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Только Администратор может создавать жанры!')
        serializer.save()

    def perform_destroy(self, serializer, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=self.kwargs.get('slug'))
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
        super(TitlesViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer, *args, **kwargs):
        instance = Title.objects.get(pk=self.kwargs.get('pk'))
        try:
            assert self.request.user.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
        #title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

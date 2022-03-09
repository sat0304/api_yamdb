from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import filters, permissions, status, viewsets

from reviews.models import Category, Genre, Titles
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ('name')

    def perform_create(self, serializer):    
        try:
            assert self.request.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Только Администратор может создавать категории!')    
        serializer.save()

    def perform_destroy(self, serializer, *args, **kwargs):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        try:
            assert self.request.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ('name')

    def perform_create(self, serializer):
        try:
            assert self.request.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Только Администратор может создавать жанры!')        
        serializer.save(author=self.request.user)

    def perform_destroy(self, serializer, *args, **kwargs):
        genre = get_object_or_404(Genre, pk=self.kwargs.get('pk'))
        try:
            assert self.request.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        try:
            assert self.request.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(TitlesViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer, *args, **kwargs):
        title = get_object_or_404(Titles, pk=self.kwargs.get('pk'))
        try:
            assert self.request.role == 'admin'
        except AssertionError:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

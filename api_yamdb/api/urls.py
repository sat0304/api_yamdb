from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='name_genres')
router_v1.register('categories', CategoryViewSet, basename='name_categories')
router_v1.register('titles', TitleViewSet, basename='name_titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include('users.urls', namespace='users')),
]

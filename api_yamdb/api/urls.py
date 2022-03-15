from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres')
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories')
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles')

urlpatterns = [
    path(
        'v1/',
        include(
            'reviews.urls',
            namespace='reviews')
    ),
    path(
        'v1/',
        include(
            'users.urls',
            namespace='users')),
    path('v1/', include(router_v1.urls)),
]

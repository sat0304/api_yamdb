from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitlesViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='name_genres')
router_v1.register('categories', CategoryViewSet, basename='name_categories')
router_v1.register('titles', TitlesViewSet, basename='name_titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

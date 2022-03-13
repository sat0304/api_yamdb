from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet

app_name = 'reviews'

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('', include(router_v1.urls)),
]

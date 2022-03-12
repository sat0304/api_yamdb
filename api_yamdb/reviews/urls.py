from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet

app_name = 'reviews'

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentViewSet,
    basename='comment'
)
urlpatterns = [
    path('', include(router_v1.urls)),
]

from django.urls import include, path
from rest_framework import routers

from .views import MyselfViewSet, SignupViewSet, TokenView, UsersViewSet

app_name = 'users'

auth_v1 = routers.DefaultRouter()
auth_v1.register(
    r'signup', SignupViewSet,
    basename='signup'
)

users_v1 = routers.DefaultRouter()
users_v1.register(
    r'', UsersViewSet,
    basename='users-list'
)


urlpatterns = [
    path(
        'auth/token/',
        TokenView,
        name='token'),
    path(
        'auth/',
        include(auth_v1.urls)),
    path(
        'users/me/',
        MyselfViewSet.as_view({'get': 'retrieve',
                               'patch': 'partial_update', }),
        name='myself'),
    path('users/', include(users_v1.urls)),
]

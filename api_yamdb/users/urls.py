from django.urls import include, path
from rest_framework import routers

from .views import SignupViewSet, TokenView, UsersViewSet

app_name = 'users'

auth_v1 = routers.DefaultRouter()
auth_v1.register(r'signup', SignupViewSet, basename='signup')

users_v1 = routers.DefaultRouter()
users_v1.register(r'', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/token/', TokenView, name='token'),
    path('auth/', include(auth_v1.urls)),
    path('users/', include(users_v1.urls)),
]

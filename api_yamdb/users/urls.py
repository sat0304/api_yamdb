from django.urls import include, path
from rest_framework import routers

from .views import SignupViewSet, TokenView

app_name = 'users'

auth_v1 = routers.DefaultRouter()
auth_v1.register(r'signup', SignupViewSet, basename='signup')


users_v1 = routers.DefaultRouter()

urlpatterns = [
    path('auth/token/', TokenView, name='token'),
    path('auth/', include(auth_v1.urls)),
    path('users/', include(users_v1.urls)),
]

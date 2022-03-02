from django.urls import include, path
from rest_framework import routers

app_name = 'users'

auth_v1 = routers.DefaultRouter()

users_v1 = routers.DefaultRouter()

urlpatterns = [
    path('auth', include(auth_v1.urls)),
    path('users', include(users_v1.urls)),
]

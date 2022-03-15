import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from .mixins import RetrieveUpdateViewSet
from .models import User
from .permissions import IsAdministratorPermission
from .serializers import SignUpSerializer, TokenSerializer, UsersViewSerializer


def generate_n_sent(email, username, flag):
    """генерирует пароль и код подтверждения. Последний отправляет на почту"""
    digit = ''.join(string.digits)
    letters = ''.join(string.ascii_letters)
    confirmation_code = ''.join(random.choice(digit) for _ in range(9))
    password = ''.join(random.choice(letters) for _ in range(9))
    content = (f'Привет {username}, \n Спасибо за использование YAMDB.'
               + f'\n Твой код подтверждения {confirmation_code}')
    if flag:
        send_mail(
            'e-mail required',
            content,
            'admin@yamdb.loc',
            (email, ),
            fail_silently=False
        )
    return confirmation_code, password


class SignupViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)

    def perform_create(self, serializer):
        flag = True
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        confirmation_code, password = generate_n_sent(email, username, flag)
        serializer.save(confirmation_code=confirmation_code, password=password)


@api_view(['POST'])
@permission_classes([AllowAny])
def TokenView(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User,
            username=request.data.get('username')
        )
        c_code = user.confirmation_code
        if request.data['confirmation_code'] == c_code:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersViewSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, )
    search_fields = ('=username',)
    permission_classes = (IsAdministratorPermission,)
    lookup_field = 'username'
    lookup_url_kwarg = 'usernamе'
    lookup_value_regex = r'[\w.@+-]+'

    def perform_create(self, serializer):
        flag = False
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        confirmation_code, password = generate_n_sent(email, username, flag)
        serializer.save(confirmation_code=confirmation_code, password=password)


class MyselfViewSet(RetrieveUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = UsersViewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.request.auth.payload.get('user_id')
        user = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, user)
        return user

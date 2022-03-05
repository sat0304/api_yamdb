import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from .models import User
from .serializers import SignUpSerializer, TokenSerializer


class SignupViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        digit = ''.join(string.digits)
        letters = ''.join(string.ascii_letters)
        confirmation_code = ''.join(random.choice(digit) for _ in range(9))
        password = ''.join(random.choice(letters) for _ in range(9))
        content = (f'Привет {username}, \n Спасибо за использование YAMDB.'
                   + f'\n Твой код подтверждения {confirmation_code}')
        send_mail(
            'e-mail required',
            content,
            'admin@yamdb.loc',
            (email, ),
            fail_silently=False
        )
        serializer.save(confirmation_code=confirmation_code, password=password)


@api_view(['POST'])
@permission_classes([AllowAny])
def TokenView(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User,
                                 username=request.data['username']
                                 )
        c_code = user.confirmation_code
        if request.data['confirmation_code'] == c_code:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ROLE_CHOICES

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email', )
        read_only_fields = ('confirmation_code',)

    def validate(self, attrs):
        username = attrs.get('username')
        if username == 'me':
            raise ValidationError('Нельзя создать пользователя с логином me')
        return super().validate(attrs)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True, max_length=9)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
            'token')

    def get_token(self, obj):
        user = get_object_or_404(
            User,
            username=self.initial_data.get('username')
        )
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UsersViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False, default='user')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        lookup_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        check_user = User.objects.filter(username=username)
        check_email = User.objects.filter(email=email)
        if check_user.exists():
            raise ValidationError('Пользователь уже существует')
        if check_email.exists():
            raise ValidationError('Почта уже существует')
        request = self.context.get('request')
        id = request.auth.payload.get('user_id')
        user = get_object_or_404(User, id=id)

        role = attrs.get('role')
        flag = True
        if role:
            flag = False
            for i in range(3):
                if ROLE_CHOICES[i][0] == role:
                    flag = True
        if not flag:
            raise ValidationError('Неправильная роль')

        if user.role == 'user' and 'role' in attrs and not user.is_superuser:
            attrs['role'] = 'user'
        return super().validate(attrs)

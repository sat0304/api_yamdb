from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', )
        read_only_fields = ('confirmation_code',)

    def validate(self, attrs):
        username = attrs['username']
        if username == 'me':
            raise ValidationError('Нельзя создать пользователя с логином me')
        return super().validate(attrs)


class TokenSerializer(serializers.ModelSerializer):
    # password = serializers.StringRelatedField(required=False)
    # read_only_fields = ('password',)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'token')
        read_only_fields = ('username', 'confirmation_code')

    def get_token(self, obj):
        user = get_object_or_404(User,
                                 username=self.initial_data['username']
                                 )
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

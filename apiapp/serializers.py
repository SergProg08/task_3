from datetime import datetime
from typing import Dict, Any, Union
from django.contrib.auth import login
from django.contrib.auth.models import update_last_login
from django.db import transaction
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from .models import MyRefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'date_joined', 'password')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        super().validate(attrs)
        refresh = self.get_token(self.user)
        if self.user.refresh_token.expired_at.timestamp() < datetime.now().timestamp():
            self.user.refresh_token.update(self.user)
        login(self.context["request"], self.user)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        data_to_display = {"refresh": str(self.user.refresh_token.value),"access": str(refresh.access_token)}
        return data_to_display


class MyTokenRefreshSerializer(TokenRefreshSerializer):

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Union[Dict[str, str], Response]:

        with transaction.atomic():

            local_refresh = attrs["refresh"]
            user = MyRefreshToken.objects.get(value=local_refresh).user
            refresh = RefreshToken.for_user(user=user)

            if user:
                if str(local_refresh) == str(user.refresh_token.value):
                    MyRefreshToken.update(user)

                    if api_settings.ROTATE_REFRESH_TOKENS:
                        if api_settings.BLACKLIST_AFTER_ROTATION:
                            try:
                                # Attempt to blacklist the given refresh token
                                refresh.blacklist()
                            except AttributeError:
                                # If blacklist app not installed, `blacklist` method will
                                # not be present
                                pass

                        refresh.set_jti()
                        refresh.set_exp()
                        refresh.set_iat()

                    data_to_display = {"refresh": str(user.refresh_token.value), "access": str(refresh.access_token)}
                    return data_to_display
            else:
                return Response({"Error": "Invalid refresh token."})


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "first_name", "last_name", "username"


class UserLogoutSerializer(serializers.ModelSerializer):

    refresh_token = serializers.CharField(source='value')

    class Meta:
        model = MyRefreshToken
        fields = ("refresh_token",)
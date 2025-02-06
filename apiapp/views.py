from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer, UserLogoutSerializer
from django.contrib.auth import logout
from .models import User, MyRefreshToken


class UserCreateAPIView(APIView):

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        email = request.data["email"]
        password = request.data["password"]
        with transaction.atomic():
            user = User.objects._create_user(email=email, password=password)
            MyRefreshToken.create(user)
            data = {
                "message": 'New user created',
                "email": email,
                "password": password,
                            }
            return Response(data, status=status.HTTP_201_CREATED)


class UserLogoutAPIView(APIView):

    serializer_class = UserLogoutSerializer

    def post(self, request: Request) -> Response:
        refresh_token = request.data["refresh_token"]
        user = request.user
        if refresh_token == str(user.refresh_token.value):
            logout(request)
        else:
            return Response({"Error": f"Invalid refresh token. Try: {user.refresh_token.value}"})
        return Response({"message": 'You`ve been logged out'})


class MeAPIView(APIView):

    serializer_class = UserUpdateSerializer

    def get(self, request: Request) -> Response:
        user = request.user
        data = {
            "message": 'You account information',
            "id": user.pk,
            "username": user.username,
            "email": user.email
        }
        return Response(data)

    def put(self, request: Request) -> Response:
        serializer = UserUpdateSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

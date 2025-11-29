from typing import Any
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_yasg.utils import swagger_auto_schema
from ..models import UserSerializer, LoginSerializer, TokenResponseSerializer, RefreshTokenParameterSerializer
from django.contrib.auth.models import AbstractUser

REGISTER_OK : str = "You have been registered successfully";
LOGOUT_OK : str = "Logout successful";
INVALID_CREDENTIALS : str = "Invalid credentials";
LOGOUT_BAD_TOKEN : str = "Invalid refresh token entered";

@swagger_auto_schema(method='post', request_body=UserSerializer, responses={201 : REGISTER_OK})
@api_view(['POST'])
def register(request : Any) -> Response:
    serializer : UserSerializer = UserSerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(REGISTER_OK, status=status.HTTP_201_CREATED);
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

@swagger_auto_schema(method='post', request_body=LoginSerializer, responses={200: TokenResponseSerializer, 401: INVALID_CREDENTIALS})
@api_view(['POST'])
def login(request):
    user : AbstractUser = authenticate(username=request.data['username'], password=request.data['password']);
    if not user:
        return Response(INVALID_CREDENTIALS, status=401);
    refresh : RefreshToken = RefreshToken.for_user(user);
    serializer : TokenResponseSerializer = TokenResponseSerializer({
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    });
    return Response(serializer.data, status=status.HTTP_201_CREATED);

@swagger_auto_schema(method='post', request_body=RefreshTokenParameterSerializer, responses={200: LOGOUT_OK})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request : Any) -> Response:
    serializer : RefreshTokenParameterSerializer = RefreshTokenParameterSerializer(data=request.data);
    if not serializer.is_valid():
        return Response(LOGOUT_BAD_TOKEN, status=status.HTTP_400_BAD_REQUEST);
    try:
        refresh_token: RefreshToken = RefreshToken(serializer.validated_data["refresh"]);
        refresh_token.blacklist();
        return Response(LOGOUT_OK, status=status.HTTP_200_OK);
    except TokenError:
        return Response(LOGOUT_BAD_TOKEN, status=status.HTTP_400_BAD_REQUEST);


@swagger_auto_schema(method='get', responses={200: UserSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request: Any) -> Response:
    """Retrieve current authenticated user profile."""
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='patch', request_body=UserSerializer, responses={200: UserSerializer, 400: 'Bad Request'})
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_profile(request: Any) -> Response:
    """Partially update current authenticated user profile."""
    user = request.user
    data = dict(request.data)
    pwd = data.pop('password', None)
    serializer = UserSerializer(instance=user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        if pwd:
            user.set_password(pwd)
            user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

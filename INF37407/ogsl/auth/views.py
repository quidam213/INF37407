from typing import Any
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from ..models import UserSerializer, LoginSerializer, TokenResponseSerializer
from django.contrib.auth.models import AbstractUser

REGISTER_OK : str = "You have been registered successfully"
LOGOUT_OK : str = "Logout successful"
INVALID_CREDENTIALS : str = "Invalid credentials"

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
def login(request : Any) -> Response:
    try:
        username : str = request.data.get('username');
        password : str = request.data.get('password');
        if not username or not password:
            return Response(INVALID_CREDENTIALS, status=status.HTTP_400_BAD_REQUEST);
        user : AbstractUser = authenticate(username=username, password=password);
        if user is not None:
            refresh : RefreshToken = RefreshToken.for_user(user);
            token : str = str(refresh.access_token);
            return Response({'token': token}, status=status.HTTP_200_OK);
        return Response(INVALID_CREDENTIALS, status=status.HTTP_401_UNAUTHORIZED);
    except Exception as e:
        return Response(INVALID_CREDENTIALS, status=status.HTTP_400_BAD_REQUEST);

@swagger_auto_schema(method='post', responses={200: LOGOUT_OK}, security=[{'Bearer': []}])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request : Any) -> Response:
    try:
        refresh_token : str = request.auth;
        if refresh_token:
            token : RefreshToken = RefreshToken(refresh_token);
            token.blacklist();
        return Response(LOGOUT_OK, status=status.HTTP_200_OK);
    except Exception as e:
        return Response(LOGOUT_OK, status=status.HTTP_200_OK);

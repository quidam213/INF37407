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

@swagger_auto_schema(method='post', responses={200: LOGOUT_OK}, security=[{'Bearer': []}])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request : Any) -> Response:
    print('Authorization header:', request.headers.get('Authorization'))
    return Response(LOGOUT_OK, status=status.HTTP_200_OK);

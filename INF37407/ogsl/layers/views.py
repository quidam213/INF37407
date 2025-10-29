from typing import Any
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Service, ServiceSerializer, Layer, LayerSerializer, ServiceIdParameterSerializer
from drf_yasg.utils import swagger_auto_schema

SERVICE_NOT_FOUND : str = "Service not found";
LAYER_NOT_FOUND : str = "Layer not found";
LAYER_DELETED_SUCCESSFULLY : str = "Layer deleted successfully";
LAYER_UPDATED_SUCCESSFULLY : str = "Layer updated successfully";
LAYER_CREATED_SUCCESSFULLY : str = "Layer created successfully";

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : LayerSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_layers_by_service_id(request : Any, service_id : int) -> Response:
    pass;

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : LayerSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_layer_by_id(request : Any, layer_id : int) -> Response:
    pass;

@swagger_auto_schema(method='delete', security=[{'Bearer': []}], responses={200 : LAYER_DELETED_SUCCESSFULLY})
@api_view(['delete'])
@permission_classes([IsAuthenticated])
def delete_layer_by_id(request : Any, layer_id : int) -> Response:
    pass;

@swagger_auto_schema(method='patch', security=[{'Bearer': []}], request_body= LayerSerializer, responses={200 : LAYER_UPDATED_SUCCESSFULLY})
@api_view(['patch'])
@permission_classes([IsAuthenticated])
def patch_layer_by_id(request : Any, layer_id : int) -> Response:
    pass;

@swagger_auto_schema(method='post', security=[{'Bearer': []}], request_body= LayerSerializer, responses={200 : LAYER_CREATED_SUCCESSFULLY})
@api_view(['post'])
@permission_classes([IsAuthenticated])
def post_layer(request : Any) -> Response:
    pass;

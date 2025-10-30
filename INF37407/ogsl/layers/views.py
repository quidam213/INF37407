from typing import Any
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Service, Layer, LayerSerializer, ServiceIdParameterSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404, get_list_or_404

LAYER_DELETED_SUCCESSFULLY : str = "Layer deleted successfully";
LAYER_UPDATED_SUCCESSFULLY : str = "Layer updated successfully";
LAYER_CREATED_SUCCESSFULLY : str = "Layer created successfully";

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : LayerSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_layers_by_service_id(request : Any, service_id : int) -> Response:
    service : Service = get_object_or_404(Service, id=service_id);
    layers : list[Layer] = get_list_or_404(Layer, service=service);
    layers_serializer : LayerSerializer = LayerSerializer(layers, many=True);
    return Response(layers_serializer.data, status=status.HTTP_200_OK);

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : LayerSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_layer_by_id(request : Any, layer_id : int) -> Response:
    layer : Layer = get_object_or_404(Layer, id=layer_id);
    serializer : LayerSerializer = LayerSerializer(layer);
    return Response(serializer.data, status=status.HTTP_200_OK);

@swagger_auto_schema(method='delete', security=[{'Bearer': []}], responses={200 : LAYER_DELETED_SUCCESSFULLY})
@api_view(['delete'])
@permission_classes([IsAuthenticated])
def delete_layer_by_id(request : Any, layer_id : int) -> Response:
    layer : Layer = get_object_or_404(Layer, id=layer_id);
    layer.delete();
    return Response(LAYER_DELETED_SUCCESSFULLY, status=status.HTTP_200_OK);

@swagger_auto_schema(method='patch', security=[{'Bearer': []}], request_body= LayerSerializer, responses={200 : LAYER_UPDATED_SUCCESSFULLY})
@api_view(['patch'])
@permission_classes([IsAuthenticated])
def patch_layer_by_id(request : Any, layer_id : int) -> Response:
    layer : Layer = get_object_or_404(Layer, id=layer_id);
    serializer : LayerSerializer = LayerSerializer(instance=layer, data=request.data, partial=True);
    if serializer.is_valid():
        serializer.save();
        return Response(LAYER_UPDATED_SUCCESSFULLY, status=status.HTTP_200_OK);
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

@swagger_auto_schema(method='post', security=[{'Bearer': []}], request_body= LayerSerializer, responses={200 : LAYER_CREATED_SUCCESSFULLY})
@api_view(['post'])
@permission_classes([IsAuthenticated])
def post_layer(request : Any) -> Response:
    serializer : LayerSerializer = LayerSerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(LAYER_CREATED_SUCCESSFULLY, status=status.HTTP_200_OK);
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

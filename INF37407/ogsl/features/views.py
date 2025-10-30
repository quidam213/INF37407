from typing import Any
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Layer, LayerIdParameterSerializer, Feature, FeatureSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404, get_list_or_404

FEATURE_DELETED_SUCCESSFULLY : str = "Feature deleted successfully";
FEATURE_UPDATED_SUCCESSFULLY : str = "Feature updated successfully";
FEATURE_CREATED_SUCCESSFULLY : str = "Feature created successfully";

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : FeatureSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_features_by_layer_id(request : Any, layer_id : int) -> Response:
    layer : Layer = get_object_or_404(Layer, id=layer_id);
    features : list[Feature] = get_list_or_404(Feature, layer=layer);
    features_serializer : FeatureSerializer = FeatureSerializer(features, many=True);
    return Response(features_serializer.data, status=status.HTTP_200_OK);

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : FeatureSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feature_by_id(request : Any, feature_id : int) -> Response:
    feature : Feature = get_object_or_404(Feature, id=feature_id);
    serializer : FeatureSerializer = FeatureSerializer(feature);
    return Response(serializer.data, status=status.HTTP_200_OK);

@swagger_auto_schema(method='delete', security=[{'Bearer': []}], responses={200 : FEATURE_DELETED_SUCCESSFULLY})
@api_view(['delete'])
@permission_classes([IsAuthenticated])
def delete_feature_by_id(request : Any, feature_id : int) -> Response:
    feature : Feature = get_object_or_404(Feature, id=feature_id);
    feature.delete();
    return Response(FEATURE_DELETED_SUCCESSFULLY, status=status.HTTP_200_OK);

@swagger_auto_schema(method='patch', security=[{'Bearer': []}], request_body= FeatureSerializer, responses={200 : FEATURE_UPDATED_SUCCESSFULLY})
@api_view(['patch'])
@permission_classes([IsAuthenticated])
def patch_feature_by_id(request : Any, feature_id : int) -> Response:
    feature : Feature = get_object_or_404(Feature, id=feature_id);
    serializer : FeatureSerializer = FeatureSerializer(instance=feature, data=request.data, partial=True);
    if serializer.is_valid():
        serializer.save();
        return Response(FEATURE_UPDATED_SUCCESSFULLY, status=status.HTTP_200_OK);
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

@swagger_auto_schema(method='post', security=[{'Bearer': []}], request_body= FeatureSerializer, responses={200 : FEATURE_CREATED_SUCCESSFULLY})
@api_view(['post'])
@permission_classes([IsAuthenticated])
def post_feature(request : Any) -> Response:
    serializer : FeatureSerializer = FeatureSerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(FEATURE_CREATED_SUCCESSFULLY, status=status.HTTP_200_OK);
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

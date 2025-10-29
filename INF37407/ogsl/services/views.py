from typing import Any
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Service, ServiceSerializer
from drf_yasg.utils import swagger_auto_schema

SERVICE_NOT_FOUND : str = "Service not found";
SERVICE_DELETED_SUCCESSFULLY : str = "Service deleted successfully";
SERVICE_UPDATED_SUCCESSFULLY : str = "Service updated successfully";
SERVICE_CREATED_SUCCESSFULLY : str = "Service created successfully";

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : ServiceSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_services(request : Any) -> Response:
    services : Any = Service.objects.all();
    services_serializer : ServiceSerializer = ServiceSerializer(services, many=True);
    return Response(services_serializer.data, status=status.HTTP_200_OK);

@swagger_auto_schema(method='get', security=[{'Bearer': []}], responses={200 : ServiceSerializer(many=True), 404 : SERVICE_NOT_FOUND})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_service_by_id(request : Any, service_id : int) -> Response:
    service : Service = Service.objects.filter(id=service_id);
    if not service.exists():
        return Response(SERVICE_NOT_FOUND, status=status.HTTP_404_NOT_FOUND);
    service_serializer : ServiceSerializer = ServiceSerializer(service, many=True);
    return Response(service_serializer.data, status=status.HTTP_200_OK);

@swagger_auto_schema(method='delete', security=[{'Bearer': []}], responses={200 : SERVICE_DELETED_SUCCESSFULLY, 404 : SERVICE_NOT_FOUND})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_service_by_id(request : Any, service_id : int) -> Response:
    service : Service = Service.objects.filter(id=service_id);
    if not service.exists():
        return Response(SERVICE_DELETED_SUCCESSFULLY, status=status.HTTP_404_NOT_FOUND);
    service.delete();
    return Response(SERVICE_NOT_FOUND, status=status.HTTP_200_OK);

@swagger_auto_schema(method='patch', security=[{'Bearer': []}], request_body=ServiceSerializer, responses={200 : SERVICE_UPDATED_SUCCESSFULLY, 404 : SERVICE_NOT_FOUND})
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_service_by_id(request : Any, service_id : int) -> Response:
    service : Service = Service.objects.filter(id=service_id).first();
    if not service:
        return Response(SERVICE_NOT_FOUND, status=status.HTTP_404_NOT_FOUND);
    serializer = ServiceSerializer(instance=service, data=request.data, partial=True);
    if serializer.is_valid():
        serializer.save();
        return Response(SERVICE_UPDATED_SUCCESSFULLY, status=status.HTTP_200_OK);
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

@swagger_auto_schema(method='post', security=[{'Bearer': []}], request_body=ServiceSerializer, responses={201 : SERVICE_CREATED_SUCCESSFULLY})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_service(request : Any) -> Response:
    serializer : ServiceSerializer = ServiceSerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(SERVICE_CREATED_SUCCESSFULLY, status=status.HTTP_201_CREATED);
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

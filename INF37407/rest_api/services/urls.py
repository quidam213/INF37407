from django.urls import path
from .views import get_all_services, get_service_by_id, delete_service_by_id, patch_service_by_id, post_service

urlpatterns = [
    path('', get_all_services),
    path('<int:service_id>/', get_service_by_id),
    path('<int:service_id>/delete/', delete_service_by_id),
    path('<int:service_id>/patch/', patch_service_by_id),
    path('post/', post_service),
]

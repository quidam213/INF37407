from django.urls import path
from .views import get_all_layers_by_service_id, get_layer_by_id, delete_layer_by_id, patch_layer_by_id, post_layer

urlpatterns = [
    path('service/<int:service_id>/', get_all_layers_by_service_id),
    path('<int:layer_id>/', get_layer_by_id),
    path('<int:layer_id>/delete/', delete_layer_by_id),
    path('<int:layer_id>/patch/', patch_layer_by_id),
    path('post/', post_layer),
]

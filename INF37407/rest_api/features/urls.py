from django.urls import path
from .views import get_all_features_by_layer_id, get_feature_by_id, delete_feature_by_id, patch_feature_by_id, post_feature

urlpatterns = [
    path('layer/<int:layer_id>/', get_all_features_by_layer_id),
    path('<int:feature_id>/', get_feature_by_id),
    path('<int:feature_id>/delete/', delete_feature_by_id),
    path('<int:feature_id>/patch/', patch_feature_by_id),
    path('post/', post_feature),
]

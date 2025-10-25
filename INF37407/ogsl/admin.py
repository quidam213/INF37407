from django.contrib import admin;
from .models import Service, Layer, Feature;

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'created_at'];
    search_fields = ['name', 'url'];
    list_filter = ['created_at'];
    readonly_fields = ['created_at'];

@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'layer_id', 'geometry_type', 'created_at'];
    list_filter = ['service', 'geometry_type', 'created_at'];
    search_fields = ['name', 'service__name', 'display_field'];
    readonly_fields = ['created_at'];
    raw_id_fields = ['service'];

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['object_id', 'layer', 'site_name', 'geometry_type', 'created_at'];
    list_filter = ['layer__service', 'layer', 'geometry_type', 'created_at'];
    search_fields = ['site_name', 'object_id', 'layer__name'];
    readonly_fields = ['latitude', 'longitude', 'created_at'];
    raw_id_fields = ['layer'];

    def latitude(self, obj):
        return obj.latitude;
    latitude.short_description = 'Latitude';

    def longitude(self, obj):
        return obj.longitude;
    longitude.short_description = 'Longitude';

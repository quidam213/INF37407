from django.db import models;
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Service(models.Model):
    id = models.AutoField(primary_key=True);
    url = models.URLField(unique=True, max_length=500);
    name = models.CharField(max_length=255, blank=True);
    description = models.TextField(blank=True);
    short_description = models.TextField(blank=True);
    copyright_text = models.TextField(blank=True);
    spatial_reference = models.IntegerField(null=True, blank=True);
    full_extent = models.JSONField(default=dict, blank=True);
    created_at = models.DateTimeField(auto_now_add=True);

    def __str__(self):
        return self.name or self.url;

    class Meta:
        db_table = 'arcgis_services';
        verbose_name = 'Service ArcGIS';
        verbose_name_plural = 'Services ArcGIS';

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service;
        fields = (
            "id",
            "url",
            "name",
            "description",
            "short_description",
            "copyright_text",
            "spatial_reference",
            "full_extent",
            "created_at"
        );

class Layer(models.Model):
    id = models.AutoField(primary_key=True);
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='layers');
    layer_id = models.IntegerField();
    name = models.CharField(max_length=255);
    display_name = models.CharField(max_length=255, blank=True);
    description = models.TextField(blank=True);
    geometry_type = models.CharField(max_length=50);
    display_field = models.CharField(max_length=100, blank=True);
    spatial_reference = models.IntegerField(null=True, blank=True);
    extent = models.JSONField(default=dict, blank=True);
    fields_definition = models.JSONField(default=list, blank=True);
    created_at = models.DateTimeField(auto_now_add=True);

    def __str__(self):
        return f"{self.service.name} - Layer {self.layer_id}: {self.name}";

    class Meta:
        db_table = 'arcgis_layers';
        verbose_name = 'Layer ArcGIS';
        verbose_name_plural = 'Layers ArcGIS';
        unique_together = ['service', 'layer_id'];
        ordering = ['service', 'layer_id'];

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer;
        fields = (
            "id",
            "service",
            "layer_id",
            "name",
            "display_name",
            "description",
            "geometry_type",
            "display_field",
            "spatial_reference",
            "extent",
            "fields_definition",
            "created_at"
        );

class Feature(models.Model):
    id = models.AutoField(primary_key=True);
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='features');
    object_id = models.IntegerField();
    site_name = models.CharField(max_length=255, blank=True);
    geometry_type = models.CharField(max_length=50);
    geometry_data = models.JSONField(default=dict, blank=True);
    attributes = models.JSONField(default=dict, blank=True);
    created_at = models.DateTimeField(auto_now_add=True);

    def __str__(self):
        return f"Feature {self.object_id} - {self.site_name or 'No name'}";

    @property
    def latitude(self):
        """Retourne la latitude depuis les attributs"""
        return self.attributes.get('decimalLatitude') or self.attributes.get('Latitude');

    @property
    def longitude(self):
        """Retourne la longitude depuis les attributs"""
        return self.attributes.get('decimalLongitude') or self.attributes.get('Longitude');

    class Meta:
        db_table = 'arcgis_features';
        verbose_name = 'Feature ArcGIS';
        verbose_name_plural = 'Features ArcGIS';
        unique_together = ['layer', 'object_id'];
        indexes = [
            models.Index(fields=['layer', 'object_id']),
            models.Index(fields=['site_name']),
        ];

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature;
        fields = (
            "id",
            "layer",
            "object_id",
            "site_name",
            "geometry_type",
            "geometry_data",
            "attributes",
            "created_at"
        );

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True);

    class Meta:
        model = User;
        fields = ('username', 'password', 'email', 'first_name', 'last_name');

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        );
        return user;

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True);
    password = serializers.CharField(required=True, write_only=True);

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password']);
        if not user:
            raise serializers.ValidationError("Invalid credentials");
        return data;

class TokenResponseSerializer(serializers.Serializer):
    refresh : str = serializers.CharField(required=True);
    access : str = serializers.CharField(required=True);

class RefreshTokenParameterSerializer(serializers.Serializer):
    refresh : str = serializers.CharField(required=True);

class ServiceIdParameterSerializer(serializers.Serializer):
    service_id : int = serializers.IntegerField(required=True);

class LayerIdParameterSerializer(serializers.Serializer):
    layer_id : int = serializers.IntegerField(required=True);

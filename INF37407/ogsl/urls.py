from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = "Un titre",
        default_version = "v1.0",
        description = "Une petite description",
    ),
    public =True,
)

urlpatterns = [
    path ("/swagger", schema_view.with_ui("swagger", cache_timeout=0), name="schema - swagger - ui"),
    path('/services', include('ogsl.services.urls')),
    path('/layers', include('ogsl.layers.urls')),
    path('/features', include('ogsl.features.urls'))
]

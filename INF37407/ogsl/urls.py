from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = "OGSL REST API",
        default_version = "v1.0",
        description = "OGSL REST API est une partie du tp 1 du cours d'inforoute avec Mr Yaddaden à l'UQAR.",
    ),
    public =True,
)

urlpatterns = [
    path ('swagger/', schema_view.with_ui("swagger", cache_timeout=0), name="schema - swagger - ui"),
    path('auth/', include('ogsl.auth.urls')),
    path('services/', include('ogsl.services.urls')),
    path('layers/', include('ogsl.layers.urls')),
    path('features/', include('ogsl.features.urls'))
]

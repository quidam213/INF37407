from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = "REST API",
        default_version = "v1.0",
        description = "" \
        "This project is a school project from our INF37407 - Technologies de l'inforoute by PhD. Yacine Yaddaden at UQAR (Université du Québec à Rimouski), QC, Canada.\n" \
        "This is the REST API part where you can manage data retrieved by the parser.",
    ),
    public =True,
)

urlpatterns = [
    path ('swagger/', schema_view.with_ui("swagger", cache_timeout=0), name="schema - swagger - ui"),
    path('auth/', include('rest_api.auth.urls')),
    path('services/', include('rest_api.services.urls')),
    path('layers/', include('rest_api.layers.urls')),
    path('features/', include('rest_api.features.urls'))
]

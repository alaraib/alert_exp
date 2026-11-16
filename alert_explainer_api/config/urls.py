from django.http import JsonResponse
from django.urls import include, path
from django.views.decorators.http import require_GET
from drf_spectacular.renderers import OpenApiJsonRenderer
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


@require_GET
def root(request):
    return JsonResponse({"status": "AI Intelligence Layer is running"})


urlpatterns = [
    path("", root, name="root"),
    path("docs", SpectacularSwaggerView.as_view(url_name="openapi-schema"), name="docs"),
    path(
        "openapi/schema/",
        SpectacularAPIView.as_view(renderer_classes=[OpenApiJsonRenderer]),
        name="openapi-schema",
    ),
    path("", include("alerts.urls")),
]
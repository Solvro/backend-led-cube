from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from modules.animations import urls as animationurls
from modules.users import urls as authurls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(authurls)),
    path("animations/", include(animationurls)),
    # API Schema and Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # OpenAPI schema
    # Swagger UI on the root path
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

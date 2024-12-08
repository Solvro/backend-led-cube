from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnimationViewSet

router = DefaultRouter()
router.register(r"", AnimationViewSet, basename="animation")

urlpatterns = [path("", include(router.urls))]

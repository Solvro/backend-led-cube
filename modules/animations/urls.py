from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimationViewSet

router = DefaultRouter()
router.register(r'animations', AnimationViewSet, basename='animation')

urlpatterns = [
    path('', include(router.urls))
]
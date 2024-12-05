from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Animation
from .serializers import AnimationSerializer

class AnimationViewSet(viewsets.ModelViewSet):

    queryset = Animation.objects.all()
    serializer_class = AnimationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the owner to the authenticated user
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Only return animations owned by the authenticated user
        return self.queryset.filter(owner=self.request.user)
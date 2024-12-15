from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Animation
from .serializers import AnimationSerializer


class AnimationViewSet(viewsets.ModelViewSet):

    queryset = Animation.objects.all()
    serializer_class = AnimationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the owner to the authenticated user
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.isStaff:
            return self.queryset

        else:
            return self.queryset.filter(owner=self.request.user)

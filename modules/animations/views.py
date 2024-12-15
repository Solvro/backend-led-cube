from rest_framework import viewsets

from modules.animations.models import Animation
from modules.animations.serializers import AnimationSerializer


class AnimationViewSet(viewsets.ModelViewSet):

    queryset = Animation.objects.all()
    serializer_class = AnimationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.isStaff:
            return self.queryset

        else:
            return self.queryset.filter(owner=self.request.user)

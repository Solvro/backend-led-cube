import django_filters
from django.contrib.auth.models import User
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from modules.animations.models import Animation
from modules.animations.serializers import AnimationSerializer


class AnimationFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="owner__username", lookup_expr="exact"
    )

    class Meta:
        model = Animation
        fields = ["username"]


class AnimationViewSet(viewsets.ModelViewSet):
    queryset = Animation.objects.all()
    serializer_class = AnimationSerializer

    @extend_schema(
        summary="Like an animation",
        description="Toggles the like status for an animation. If already liked, it unlikes it.",
        parameters=[
            OpenApiParameter(name="id", description="Animation ID", required=True, type=int),
        ],
        responses={
            200: OpenApiResponse(description="Liked/Unliked"),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):
        animation = self.get_object()
        user = request.user

        if user in animation.liked_by.all():
            animation.liked_by.remove(user)  # Unlike
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        else:
            animation.liked_by.add(user)  # Like
            return Response({"message": "Liked"}, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter animations by the username of the owner.",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")

        if username:
            try:
                user = User.objects.get(username=username)
                queryset = queryset.filter(owner=user)
            except User.DoesNotExist:
                raise NotFound({"detail": "User not found."})

        return queryset

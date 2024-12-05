from rest_framework import serializers
from .models import Animation

class AnimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = ['id', 'owner', 'name', 'description', 'animation']
        read_only_fields = ['id', 'owner']

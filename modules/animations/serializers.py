from rest_framework import serializers

from modules.animations.models import Animation


class AnimationSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(
        source="owner.username", read_only=True
    )

    class Meta:
        model = Animation
        fields = ["id", "owner", "name", "description", "animation"]
        read_only_fields = ["id", "owner"]

    def validate_animation(self, value):
        if len(value) > 10_000:
            raise serializers.ValidationError("Animation code is too long.")

        suspicious_tokens = ["require(", "fs.", "child_process", "import "]
        if any(token in value for token in suspicious_tokens):
            raise serializers.ValidationError(
                "Suspicious tokens found in animation code."
            )

        return value

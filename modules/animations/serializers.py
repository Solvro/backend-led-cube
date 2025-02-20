from rest_framework import serializers

from modules.animations.models import Animation


def get_like_count(obj):
    return obj.liked_by.count()


def validate_animation(value):
    if len(value) > 10_000:
        raise serializers.ValidationError("Animation code is too long.")

    suspicious_tokens = ["require(", "fs.", "child_process", "import "]
    if any(token in value for token in suspicious_tokens):
        raise serializers.ValidationError("Suspicious tokens found in animation code.")

    return value


class AnimationSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        return user in obj.liked_by.all() if user.is_authenticated else False

    def get_like_count(self, obj):
        return obj.liked_by.count()

    class Meta:
        model = Animation
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "animation",
            "like_count",
            "is_liked",
        ]
        read_only_fields = ["id", "owner"]

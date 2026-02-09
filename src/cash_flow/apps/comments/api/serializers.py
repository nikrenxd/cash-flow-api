from rest_framework import serializers

from src.cash_flow.apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "body", "created_at", "updated_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("body",)


class CommentUpdateSerializer(CommentCreateSerializer):
    pass

from rest_framework import serializers

from src.cash_flow.apps.users.models import CustomUser as User


class UserCreateSerializer(serializers.ModelSerializer[User]):
    class Meta:
        fields = ["email", "password"]
        model = User
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserActivateResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)
    activated = serializers.BooleanField(read_only=True)


class UserNotActivateResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)
    activated = serializers.BooleanField(read_only=True, default=False)

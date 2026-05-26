from rest_framework import serializers

from src.cash_flow.apps.statuses.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            "id",
            "name",
            "description",
        )


class StatusCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ("name", "description")


class StatusUpdateSerializer(StatusCreateSerializer):
    pass

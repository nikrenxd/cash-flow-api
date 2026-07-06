from rest_framework import serializers

from cash_flow.apps.statuses.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            "id",
            "name",
            "description",
        )


class StatusTransactionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField()
    created_at = serializers.DateTimeField()


class StatusDetailSerializer(serializers.ModelSerializer):
    transactions = StatusTransactionsSerializer(many=True)

    class Meta:
        model = Status
        fields = (
            "name",
            "description",
            "transactions",
        )


class StatusCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ("name", "description")


class StatusUpdateSerializer(StatusCreateSerializer):
    pass

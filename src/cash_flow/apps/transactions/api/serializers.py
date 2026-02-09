import datetime

from rest_framework import serializers

from src.cash_flow.apps.transactions.models import Transaction


class TransactionCommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    body = serializers.CharField(max_length=30)


class TransactionSerializer(serializers.ModelSerializer):
    comments = TransactionCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "date",
            "comments",
            "created_at",
            "updated_at",
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    transaction_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Transaction
        fields = ("amount", "transaction_date")

    def validate_transaction_date(self, value: datetime.date) -> datetime.date:
        if value is not None and value > datetime.date.today():
            raise serializers.ValidationError(
                "Transaction date cannot be in the future"
            )

        return value


class TransactionUpdateSerializer(TransactionCreateSerializer):
    pass

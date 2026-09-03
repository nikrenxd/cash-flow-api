import datetime

from rest_framework import serializers

from cash_flow.apps.transactions.models import Transaction


class TransactionCommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    body = serializers.CharField(max_length=30)


class TransactionStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class TransactionTransactionTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class TransactionSubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class TransactionCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class TransactionSerializer(serializers.ModelSerializer):
    status = TransactionStatusSerializer(read_only=True)
    transaction_type = TransactionTransactionTypeSerializer(
        read_only=True,
        source="subcategory.category.transaction_type",
    )
    subcategory = TransactionSubcategorySerializer(read_only=True)
    category = TransactionCategorySerializer(
        read_only=True,
        source="subcategory.category",
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "date",
            "transaction_type",
            "subcategory",
            "category",
            "status",
            "created_at",
            "updated_at",
        )


class TransactionDetailSerializer(serializers.ModelSerializer):
    status = TransactionStatusSerializer(read_only=True)
    comments = TransactionCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "date",
            "status",
            "comments",
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    transaction_date = serializers.DateField(
        required=False,
        allow_null=True,
    )
    status_id = serializers.IntegerField(required=True, allow_null=False)
    subcategory_id = serializers.IntegerField(required=True, allow_null=False)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "transaction_date",
            "status_id",
            "subcategory_id",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate_transaction_date(self, value: datetime.date) -> datetime.date:
        if value is not None and value > datetime.date.today():
            raise serializers.ValidationError(
                "Transaction date cannot be in the future"
            )

        return value

    def to_representation(self, instance: Transaction) -> dict:
        data = super().to_representation(instance)
        data["transaction_date"] = instance.date

        return data


class TransactionUpdateSerializer(TransactionCreateSerializer):
    pass

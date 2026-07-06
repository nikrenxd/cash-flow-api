from rest_framework import serializers

from cash_flow.apps.categories.models import Category
from cash_flow.apps.transaction_types.api.serializers import (
    TransactionTypeSerializer,
)


class CategorySerializer(serializers.ModelSerializer):
    transaction_type = TransactionTypeSerializer()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "transaction_type",
        )


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class CategoryUpdateSerializer(serializers.ModelSerializer):
    transaction_type_id = serializers.IntegerField(required=True, allow_null=False)

    class Meta:
        model = Category
        fields = (
            "name",
            "transaction_type_id",
        )

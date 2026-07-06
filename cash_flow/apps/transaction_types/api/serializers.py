from rest_framework import serializers

from cash_flow.apps.transaction_types.models import TransactionType


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = (
            "id",
            "name",
            "description",
            "created_at",
        )


class TransactionTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = (
            "name",
            "description",
        )


class TransactionTypeCategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()


class TransactionTypeDetailSerializer(serializers.ModelSerializer):
    categories = TransactionTypeCategoriesSerializer(many=True, read_only=True)

    class Meta:
        model = TransactionType
        fields = ("name", "description", "categories", "created_at", "updated_at")


class TransactionTypeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = (
            "name",
            "description",
        )
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False, "allow_blank": True},
        }

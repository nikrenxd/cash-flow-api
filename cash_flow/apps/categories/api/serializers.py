from rest_framework import serializers

from cash_flow.apps.categories.models import Category


class CategoryTransactionTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    transaction_type = CategoryTransactionTypeSerializer()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "transaction_type",
        )


class CategorySubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CategoryDetailSerializer(serializers.ModelSerializer):
    transaction_type = CategoryTransactionTypeSerializer()
    subcategories = CategorySubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "transaction_type",
            "subcategories",
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

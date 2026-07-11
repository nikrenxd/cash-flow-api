from rest_framework import serializers

from cash_flow.apps.subcategories.models import Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ("id", "name")


class SubcategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ("name",)


class SubcategoryUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=True, allow_null=False)

    class Meta:
        model = Subcategory
        fields = ("name", "category_id")

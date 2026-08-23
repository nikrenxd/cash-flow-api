from rest_framework import serializers

from cash_flow.apps.subcategories.models import Subcategory


class SubcategoryCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class SubcategorySerializer(serializers.ModelSerializer):
    category = SubcategoryCategorySerializer()

    class Meta:
        model = Subcategory
        fields = ("id", "name", "category")


class SubcategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ("name",)


class SubcategoryUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=True, allow_null=False)

    class Meta:
        model = Subcategory
        fields = ("name", "category_id")

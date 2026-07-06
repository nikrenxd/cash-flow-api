from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cash_flow.apps.categories.api.serializers import (
    CategoryCreateSerializer,
    CategorySerializer,
    CategoryUpdateSerializer,
)
from cash_flow.apps.categories.permissions import (
    IsTransactionTypeBelongToUser,
)
from cash_flow.apps.categories.selectors import CategorySelector
from cash_flow.apps.categories.services import CategoryService
from cash_flow.common.permissions import (
    IsOwnerOrDefaultObjectPermission,
)


@extend_schema(tags=["categories"])
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrDefaultObjectPermission,
        IsTransactionTypeBelongToUser,
    )

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return CategorySelector().none_category()

        return CategorySelector().list_categories(
            user_id=self.request.user.id,
            transaction_type_id=self.kwargs.get("transaction_type_id"),
        )

    def get_serializer_class(self):
        match self.action:
            case "create":
                return CategoryCreateSerializer
            case "update":
                return CategoryUpdateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data

        serializer.instance = CategoryService().create_category(
            category_name=data["name"],
            transaction_type_id=self.kwargs["transaction_type_id"],
            user_id=self.request.user.id,
        )

    def perform_update(self, serializer):
        data = serializer.validated_data
        category_to_update = serializer.instance

        serializer.instance = CategoryService().update_category(
            category=category_to_update,
            category_name=data.get("name", None),
            transaction_type_id=data.get("transaction_type_id", None),
        )

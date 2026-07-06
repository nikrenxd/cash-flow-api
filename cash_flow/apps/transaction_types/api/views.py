from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cash_flow.apps.transaction_types.api.serializers import (
    TransactionTypeCreateSerializer,
    TransactionTypeDetailSerializer,
    TransactionTypeSerializer,
    TransactionTypeUpdateSerializer,
)
from cash_flow.apps.transaction_types.selectors import TransactionTypeSelector
from cash_flow.apps.transaction_types.services import TransactionTypeService
from cash_flow.common.permissions import (
    IsOwnerOrDefaultObjectPermission,
)


@extend_schema(tags=["transaction types"])
class TransactionTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionTypeSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrDefaultObjectPermission,
    )

    def get_queryset(self):
        return TransactionTypeSelector().list_transaction_types(
            user_id=self.request.user.id,
        )

    def get_serializer_class(self):
        match self.action:
            case "create":
                return TransactionTypeCreateSerializer
            case "update":
                return TransactionTypeUpdateSerializer
            case "retrieve":
                return TransactionTypeDetailSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data
        serializer.instance = TransactionTypeService().create_transaction_type(
            tt_name=data["name"],
            tt_description=data.get("description", None),
            user_id=self.request.user.id,
        )

    def perform_update(self, serializer):
        data = serializer.validated_data
        transaction_type_to_update = serializer.instance

        serializer.instance = TransactionTypeService().update_transaction_type(
            transaction_type=transaction_type_to_update,
            tt_name=data.get("name", None),
            tt_description=data.get("description", None),
        )

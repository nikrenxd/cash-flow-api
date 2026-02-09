import logging

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.cash_flow.apps.transactions.api.serializers import (
    TransactionCreateSerializer,
    TransactionSerializer,
    TransactionUpdateSerializer,
)
from src.cash_flow.apps.transactions.selectors import TransactionSelector
from src.cash_flow.apps.transactions.services import TransactionService
from src.cash_flow.common.permissions import IsOwnerPermission

logger = logging.getLogger(__name__)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, IsOwnerPermission)
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.action == "list":
            return TransactionSelector().list_transactions_comments(
                self.request.user.id,
            )
        return TransactionSelector().list_transactions(user_id=self.request.user.id)

    def get_serializer_class(self):
        match self.action:
            case "create":
                return TransactionCreateSerializer
            case "partial_update":
                return TransactionUpdateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data
        user_id = self.request.user.id
        data["user_id"] = user_id

        serializer.instance = TransactionService().create_transaction(**data)

    def perform_update(self, serializer):
        data = serializer.validated_data
        transaction = serializer.instance
        serializer.instance = TransactionService().update_transaction(
            transaction,
            **data,
        )

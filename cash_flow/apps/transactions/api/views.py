import logging

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from cash_flow.apps.statuses.exceptions import StatusObjectDoesNotExist
from cash_flow.apps.transactions.api.serializers import (
    TransactionCreateSerializer,
    TransactionDetailSerializer,
    TransactionSerializer,
    TransactionUpdateSerializer,
)
from cash_flow.apps.transactions.exceptions import (
    TransactionBadRequest,
    TransactionCreationError,
    TransactionUpdateError,
)
from cash_flow.apps.transactions.selectors import TransactionSelector
from cash_flow.apps.transactions.services import TransactionService
from cash_flow.common.permissions import IsOwnerPermission

logger = logging.getLogger(__name__)


@extend_schema(tags=["transactions"])
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, IsOwnerPermission)
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.action == "retrieve":
            return TransactionSelector().list_transactions_comments(
                self.request.user.id,
            )
        return TransactionSelector().list_transactions(user_id=self.request.user.id)

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return TransactionDetailSerializer
            case "create":
                return TransactionCreateSerializer
            case "partial_update":
                return TransactionUpdateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data
        user_id = self.request.user.id
        data["user_id"] = user_id

        try:
            new_transaction = TransactionService().create_transaction(**data)
            serializer.instance = new_transaction
        except TransactionCreationError as e:
            raise TransactionBadRequest from e
        except StatusObjectDoesNotExist as e:
            raise NotFound("Status not found") from e

    def perform_update(self, serializer):
        data = serializer.validated_data
        transaction = serializer.instance

        try:
            serializer.instance = TransactionService().update_transaction(
                transaction,
                **data,
            )
        except TransactionUpdateError as e:
            raise TransactionBadRequest from e
        except StatusObjectDoesNotExist as e:
            raise NotFound("Status not found") from e

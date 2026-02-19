from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.cash_flow.apps.comments.api.serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)
from src.cash_flow.apps.comments.permissions import IsAllowedAddCommentsToTransaction
from src.cash_flow.apps.comments.selectors import CommentSelector
from src.cash_flow.apps.comments.services import CommentService
from src.cash_flow.common.permissions import IsOwnerPermission


@extend_schema(tags=["comments"])
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerPermission,
        IsAllowedAddCommentsToTransaction,
    )

    def get_queryset(self):
        return CommentSelector().list_transaction_comments(
            user_id=self.request.user.id,
            transaction_id=self.kwargs["transaction_id"],
        )

    def get_serializer_class(self):
        match self.action:
            case "create":
                return CommentCreateSerializer
            case "update":
                return CommentUpdateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data
        comment = CommentService().create_comment(
            user_id=self.request.user.id,
            transaction_id=self.kwargs["transaction_id"],
            **data,
        )

        serializer.instance = comment

    def perform_update(self, serializer):
        data = serializer.validated_data
        serializer.instance = CommentService().update_comment(**data)

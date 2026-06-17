from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cash_flow.apps.comments.api.serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)
from cash_flow.apps.comments.exceptions import (
    CommentActionFailed,
    CommentCreationFailed,
    CommentUpdateFailed,
)
from cash_flow.apps.comments.permissions import IsAllowedAddCommentsToTransaction
from cash_flow.apps.comments.selectors import CommentSelector
from cash_flow.apps.comments.services import CommentService
from cash_flow.common.permissions import IsOwnerPermission


@extend_schema(
    tags=["comments"],
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location="path",
        )
    ],
)
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerPermission,
        IsAllowedAddCommentsToTransaction,
    )

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return CommentSelector().none_comment()

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

        try:
            comment = CommentService().create_comment(
                user_id=self.request.user.id,
                transaction_id=self.kwargs["transaction_id"],
                **data,
            )

            serializer.instance = comment
        except CommentActionFailed:
            raise CommentCreationFailed(detail="Comment creation failed")

    def perform_update(self, serializer):
        data = serializer.validated_data

        try:
            serializer.instance = CommentService().update_comment(**data)
        except CommentActionFailed:
            raise CommentUpdateFailed(detail="Comment update failed")

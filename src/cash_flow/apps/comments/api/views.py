from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from src.cash_flow.apps.comments.api.serializers import (
    CommentCreateSerializer,
    CommentUpdateSerializer,
)
from src.cash_flow.apps.comments.selectors import CommentSelector
from src.cash_flow.apps.comments.services import CommentService
from src.cash_flow.common.permissions import IsOwnerPermission


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CommentSelector().list_transaction_comments(
            user_id=self.request.user.id,
            transaction_id=self.kwargs["transaction_id"],
        )

    def get_serializer_class(self):
        match self.request.method:
            case "post":
                return CommentCreateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data
        comment = CommentService().create_comment(
            user_id=self.request.user.id,
            transaction_id=self.kwargs["transaction_id"],
            **data,
        )

        serializer.instance = comment


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = CommentUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerPermission)

    def get_queryset(self):
        return CommentSelector().list_comments(
            user_id=self.request.user.id,
        )

    def perform_update(self, serializer):
        data = serializer.validated_data
        serializer.instance = CommentService().update_comment(**data)

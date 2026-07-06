from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from cash_flow.apps.statuses.api.serializers import (
    StatusCreateSerializer,
    StatusDetailSerializer,
    StatusSerializer,
    StatusUpdateSerializer,
)
from cash_flow.apps.statuses.filters import StatusFilter
from cash_flow.apps.statuses.selectors import StatusSelector
from cash_flow.apps.statuses.services import StatusService
from cash_flow.common.permissions import (
    IsOwnerOrDefaultObjectPermission,
)


@extend_schema(tags=["statuses"])
class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    filterset_class = StatusFilter
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrDefaultObjectPermission,
    )

    def get_queryset(self):
        user_id = self.request.user.id
        if self.action == "list_custom_statuses":
            return StatusSelector().list_custom_statuses(user_id=user_id)

        return StatusSelector().list_default_statuses(user_id=user_id)

    def get_serializer_class(self):
        match self.action:
            case "create":
                return StatusCreateSerializer
            case "partial_update":
                return StatusUpdateSerializer
            case "retrieve":
                return StatusDetailSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data
        data["user_id"] = self.request.user.id

        serializer.instance = StatusService().create_status(**data)

    def perform_update(self, serializer):
        data = serializer.validated_data
        status_for_update = serializer.instance

        serializer.instance = StatusService().update_status(
            status=status_for_update,
            **data,
        )

    @extend_schema(
        tags=["statuses"],
        parameters=[OpenApiParameter("name", OpenApiTypes.STR, "query")],
    )
    @action(detail=False, methods=["GET"], url_path="user-statuses")
    def list_custom_statuses(self, request: Request):
        user_statuses = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(user_statuses, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

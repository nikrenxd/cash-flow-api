from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from cash_flow.apps.statuses.api.serializers import (
    StatusCreateSerializer,
    StatusDetailSerializer,
    StatusSerializer,
    StatusUpdateSerializer,
)
from cash_flow.apps.statuses.dto import CreateStatusDto, UpdateStatusDto
from cash_flow.apps.statuses.filters import StatusFilter
from cash_flow.apps.statuses.selectors import StatusSelector
from cash_flow.apps.statuses.services.status import StatusService
from cash_flow.apps.statuses.services.status_cache import StatusCache
from cash_flow.common.permissions import (
    IsOwnerOrDefaultObjectPermission,
)


class StatusPageNumberPagination(PageNumberPagination):
    page_size = 10


@extend_schema(tags=["statuses"])
class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    filterset_class = StatusFilter
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrDefaultObjectPermission,
    )
    pagination_class = StatusPageNumberPagination
    http_method_names = ["get", "post", "patch", "delete"]

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
        user_id = self.request.user.id
        dto = CreateStatusDto(user_id=user_id, **data)

        serializer.instance = StatusService().create_status(data=dto)
        StatusCache().invalidate_status_cache(user_id=user_id)

    def perform_update(self, serializer):
        data = serializer.validated_data
        dto = UpdateStatusDto(**data)
        status_for_update = serializer.instance

        serializer.instance = StatusService().update_status(
            status=status_for_update,
            data=dto,
        )
        StatusCache().invalidate_status_cache(user_id=self.request.user.id)

    def perform_destroy(self, instance):
        StatusCache().invalidate_status_cache(user_id=self.request.user.id)
        instance.delete()

    def list(self, request: Request, *args, **kwargs) -> Response:
        cache = StatusCache()
        response = cache.read_status_cache(
            user_id=self.request.user.id,
            query_params=self.request.query_params,
        )
        if response is None:
            response = super().list(request, *args, **kwargs)
            cache.set_status_cache(
                response_data=response.data,
                user_id=self.request.user.id,
                query_params=self.request.query_params,
            )
            return response

        return Response(data=response)

    @extend_schema(
        tags=["statuses"],
        parameters=[OpenApiParameter("name", OpenApiTypes.STR, "query")],
    )
    @action(detail=False, methods=["GET"], url_path="user-statuses")
    def list_custom_statuses(self, request: Request):
        user_statuses = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(user_statuses, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

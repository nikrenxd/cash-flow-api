from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cash_flow.apps.subcategories.api.serializers import (
    SubcategoryCreateSerializer,
    SubcategorySerializer,
    SubcategoryUpdateSerializer,
)
from cash_flow.apps.subcategories.dto import (
    CreateSubcategoryDto,
    UpdateSubcategoryDto,
)
from cash_flow.apps.subcategories.permissions import IsCategoryBelongsToUser
from cash_flow.apps.subcategories.selectors import SubcategorySelector
from cash_flow.apps.subcategories.services import SubcategoryService
from cash_flow.common.permissions import IsOwnerPermission


@extend_schema(tags=["subcategories"])
class SubcategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsOwnerPermission,
        IsCategoryBelongsToUser,
    )
    serializer_class = SubcategorySerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return SubcategorySelector().list_subcategories(
            user_id=self.request.user.id,
            category_id=self.kwargs.get("category_id"),
        )

    def get_serializer_class(self):
        match self.action:
            case "create":
                return SubcategoryCreateSerializer
            case "update":
                return SubcategoryUpdateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        data = serializer.validated_data
        dto = CreateSubcategoryDto(
            user_id=self.request.user.id,
            category_id=self.kwargs.get("category_id"),
            **data,
        )
        serializer.instance = SubcategoryService().create_subcategory(data=dto)

    def perform_update(self, serializer):
        data = serializer.validated_data
        dto = UpdateSubcategoryDto(**data)
        subcategory_to_update = serializer.instance

        serializer.instance = SubcategoryService().update_subcategory(
            subcategory=subcategory_to_update,
            data=dto,
        )

from django.urls import include, path
from rest_framework import routers

from cash_flow.apps.subcategories.api.views import SubcategoryViewSet

subcategories_router = routers.DefaultRouter()

subcategories_router.register(
    "subcategories",
    SubcategoryViewSet,
    basename="subcategories",
)

urlpatterns = [
    path("categories/<int:subcategory_id>/", include(subcategories_router.urls)),
]

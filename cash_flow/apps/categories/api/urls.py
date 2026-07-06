from django.urls import include, path
from rest_framework import routers

from cash_flow.apps.categories.api.views import CategoryViewSet

categories_router = routers.DefaultRouter()

categories_router.register(
    "categories",
    CategoryViewSet,
    basename="categories",
)

urlpatterns = [
    path(
        "transaction-types/<int:transaction_type_id>/",
        include(categories_router.urls),
    ),
]

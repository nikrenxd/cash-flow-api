from rest_framework import routers

from cash_flow.apps.transaction_types.api.views import TransactionTypeViewSet

transaction_types_router = routers.DefaultRouter()

transaction_types_router.register(
    "transaction-types", TransactionTypeViewSet, basename="transaction-types"
)

urlpatterns = transaction_types_router.urls

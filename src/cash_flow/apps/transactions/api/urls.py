from rest_framework import routers

from src.cash_flow.apps.transactions.api.views import TransactionViewSet

transactions_router = routers.DefaultRouter()
transactions_router.register(
    "transactions", TransactionViewSet, basename="transactions"
)

urlpatterns = transactions_router.urls

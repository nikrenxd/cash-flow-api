from rest_framework import permissions
from rest_framework.exceptions import NotFound

from src.cash_flow.apps.transactions.exceptions import TransactionObjectDoesNotExist
from src.cash_flow.apps.transactions.selectors import TransactionSelector


class IsAllowedAddCommentsToTransaction(permissions.BasePermission):
    def has_permission(self, request, view) -> bool | None:
        if view.kwargs.get("transaction_id") is None:
            return False

        try:
            transaction = TransactionSelector().get_transaction(
                transaction_id=view.kwargs.get("transaction_id")
            )
            return request.user.id == transaction.user.id
        except TransactionObjectDoesNotExist:
            raise NotFound

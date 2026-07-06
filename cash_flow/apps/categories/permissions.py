from rest_framework import permissions
from rest_framework.exceptions import NotFound

from cash_flow.apps.transaction_types.exceptions import (
    TransactionTypeObjectDoesNotExist,
)
from cash_flow.apps.transaction_types.selectors import TransactionTypeSelector


class IsTransactionTypeBelongToUser(permissions.BasePermission):
    def has_permission(self, request, view):
        transaction_type_id = view.kwargs.get("transaction_type_id")
        if transaction_type_id is None:
            return False

        try:
            transaction_type = TransactionTypeSelector().get_transaction_type(
                tt_id=transaction_type_id
            )

            # if transaction type is default allow to use it
            if transaction_type.user is None:
                return True

            return request.user.id == transaction_type.user.id
        except TransactionTypeObjectDoesNotExist as e:
            raise NotFound from e

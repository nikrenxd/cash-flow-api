from django.db.models import QuerySet

from cash_flow.apps.transactions.exceptions import TransactionObjectDoesNotExist
from cash_flow.apps.transactions.models import Transaction


class TransactionSelector:
    def list_transactions(self, user_id: int) -> QuerySet[Transaction]:
        return Transaction.objects.select_related("user", "status").filter(
            user=user_id
        )

    def list_transactions_comments(self, user_id: int) -> QuerySet[Transaction]:
        return self.list_transactions(user_id).prefetch_related("comments")

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        try:
            return Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist as e:
            raise TransactionObjectDoesNotExist from e

    def is_transaction_exists(self, transaction_id: int, user_id: int) -> bool:
        return Transaction.objects.filter(id=transaction_id, user=user_id).exists()

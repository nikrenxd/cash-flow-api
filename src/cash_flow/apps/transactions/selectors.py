from django.db.models import QuerySet

from src.cash_flow.apps.transactions.models import Transaction


class TransactionSelector:
    def list_transactions(self, user_id: int) -> QuerySet[Transaction]:
        return Transaction.objects.select_related("user").filter(user=user_id)

    def list_transactions_comments(self, user_id: int) -> QuerySet[Transaction]:
        return self.list_transactions(user_id).prefetch_related("comments")

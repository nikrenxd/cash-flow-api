from django.db.models import Q, QuerySet

from cash_flow.apps.transaction_types.models import TransactionType


class TransactionTypeSelector:
    def list_transaction_types(self, user_id: int) -> QuerySet[TransactionType]:
        return TransactionType.objects.filter(Q(user_id=None) | Q(user_id=user_id))

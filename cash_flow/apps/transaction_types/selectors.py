from django.db.models import Prefetch, Q, QuerySet

from cash_flow.apps.categories.models import Category
from cash_flow.apps.transaction_types.exceptions import (
    TransactionTypeObjectDoesNotExist,
)
from cash_flow.apps.transaction_types.models import TransactionType


class TransactionTypeSelector:
    def list_transaction_types(self, user_id: int) -> QuerySet[TransactionType]:
        return TransactionType.objects.prefetch_related(
            Prefetch(
                "categories",
                queryset=Category.objects.filter(
                    Q(user_id=None) | Q(user_id=user_id)
                ),
            )
        ).filter(
            Q(user_id=None) | Q(user_id=user_id),
        )

    def get_transaction_type(self, tt_id: int) -> TransactionType:
        try:
            return TransactionType.objects.get(id=tt_id)
        except TransactionType.DoesNotExist as e:
            raise TransactionTypeObjectDoesNotExist from e

    def is_transaction_type_exist(self, tt_id: int, user_id: int) -> bool:
        return TransactionType.objects.filter(id=tt_id, user_id=user_id).exists()

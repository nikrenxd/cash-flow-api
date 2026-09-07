from django.db import transaction

from cash_flow.apps.transaction_types.dto import (
    TransactionTypeCreateDto,
    TransactionTypeUpdateDto,
)
from cash_flow.apps.transaction_types.models import TransactionType


class TransactionTypeService:
    @transaction.atomic
    def create_transaction_type(
        self,
        data: TransactionTypeCreateDto,
    ) -> TransactionType:
        new_transaction_type = TransactionType(
            name=data.name,
            description=data.description,
            user_id=data.user_id,
        )

        new_transaction_type.full_clean()
        new_transaction_type.save()

        return new_transaction_type

    @transaction.atomic
    def update_transaction_type(
        self,
        transaction_type: TransactionType,
        data: TransactionTypeUpdateDto,
    ) -> TransactionType:
        if data.name is not None:
            transaction_type.name = data.name
        if data.description is not None:
            transaction_type.description = data.description

        transaction_type.full_clean()
        transaction_type.save()

        return transaction_type

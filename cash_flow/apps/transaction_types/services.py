from cash_flow.apps.transaction_types.models import TransactionType


class TransactionTypeService:
    def create_transaction_type(
        self,
        tt_name: str,
        user_id: int | None = None,
        tt_description: str | None = None,
    ) -> TransactionType:
        new_transaction_type = TransactionType(
            name=tt_name,
            description=tt_description,
            user_id=user_id,
        )

        new_transaction_type.full_clean()
        new_transaction_type.save()

        return new_transaction_type

    def update_transaction_type(
        self,
        transaction_type: TransactionType,
        tt_name: str | None = None,
        tt_description: str | None = None,
    ) -> TransactionType:
        if tt_name is not None:
            transaction_type.name = tt_name
        if tt_description is not None:
            transaction_type.description = tt_description

        transaction_type.full_clean()
        transaction_type.save()

        return transaction_type

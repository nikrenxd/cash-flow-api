import logging

from django.db import transaction

from cash_flow.apps.statuses.models import Status
from cash_flow.apps.statuses.selectors import StatusSelector
from cash_flow.apps.subcategories.models import Subcategory
from cash_flow.apps.subcategories.selectors import SubcategorySelector
from cash_flow.apps.transactions.dto import (
    TransactionCreateDto,
    TransactionUpdateDto,
)
from cash_flow.apps.transactions.exceptions import (
    TransactionCreationError,
    TransactionUpdateError,
)
from cash_flow.apps.transactions.models import Transaction

logger = logging.getLogger(__name__)


class TransactionService:
    def _ensure_status_belongs_to_user(
        self,
        status_id: int,
        user_id: int,
    ) -> Status | None:
        status = StatusSelector().get_status_by_id(_id=status_id)

        if status.user is not None and status.user.id != user_id:
            logger.error(f"Failed to obtain status for user: {user_id}")
            return None

        return status

    def _ensure_subcategory_belongs_to_user(
        self,
        subcategory_id: int,
        user_id: int,
    ) -> Subcategory | None:
        subcategory = SubcategorySelector().get_subcategory_by_id(_id=subcategory_id)
        if subcategory.user_id != user_id:
            logger.error(f"Failed to obtain subcategory for user: {user_id}")
            return None

        return subcategory

    @transaction.atomic
    def create_transaction(self, data: TransactionCreateDto) -> Transaction:
        logger.info(f"Creating new transaction for user with id: {data.user_id}")

        status = self._ensure_status_belongs_to_user(data.status_id, data.user_id)
        if not status:
            raise TransactionCreationError("Failed to create new transaction")

        subcategory = self._ensure_subcategory_belongs_to_user(
            data.subcategory_id,
            data.user_id,
        )
        if not subcategory:
            raise TransactionCreationError("Failed to create new transaction")

        new_transaction = Transaction(
            amount=data.amount,
            date=data.transaction_date,
            user_id=data.user_id,
            status=status,
            subcategory=subcategory,
        )

        new_transaction.full_clean()
        new_transaction.save()

        return new_transaction

    @transaction.atomic
    def update_transaction(
        self,
        transaction_to_update: Transaction,
        data: TransactionUpdateDto,
    ) -> Transaction:
        logger.info(f"Updating transaction with new amount: {data.amount}")

        if data.status_id is not None:
            status = self._ensure_status_belongs_to_user(
                data.status_id,
                transaction_to_update.user_id,
            )
            if not status:
                raise TransactionUpdateError("Failed to update transaction")
            transaction_to_update.status = status

        if data.subcategory_id is not None:
            subcategory = self._ensure_subcategory_belongs_to_user(
                data.subcategory_id,
                transaction_to_update.user_id,
            )
            if not subcategory:
                raise TransactionUpdateError("Failed to update transaction")
            transaction_to_update.subcategory = subcategory

        if data.amount is not None:
            transaction_to_update.amount = data.amount

        if data.transaction_date is not None:
            transaction_to_update.date = data.transaction_date

        transaction_to_update.full_clean()
        transaction_to_update.save()

        return transaction_to_update

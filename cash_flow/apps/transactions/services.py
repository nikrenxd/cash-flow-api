import logging
from datetime import date
from decimal import Decimal

from django.db import transaction

from cash_flow.apps.statuses.models import Status
from cash_flow.apps.statuses.selectors import StatusSelector
from cash_flow.apps.subcategories.models import Subcategory
from cash_flow.apps.subcategories.selectors import SubcategorySelector
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
    def create_transaction(
        self,
        amount: Decimal,
        user_id: int,
        status_id: int,
        subcategory_id: int,
        transaction_date: date | None = None,
    ) -> Transaction:
        logger.info(f"Creating new transaction for user with id: {user_id}")

        status = self._ensure_status_belongs_to_user(status_id, user_id)
        if not status:
            raise TransactionCreationError("Failed to create new transaction")

        subcategory = self._ensure_subcategory_belongs_to_user(
            subcategory_id,
            user_id,
        )
        if not subcategory:
            raise TransactionCreationError("Failed to create new transaction")

        new_transaction = Transaction(
            amount=amount,
            date=transaction_date,
            user_id=user_id,
            status=status,
            subcategory=subcategory,
        )

        new_transaction.full_clean()
        new_transaction.save()

        return new_transaction

    @transaction.atomic
    def update_transaction(
        self,
        _transaction: Transaction,
        status_id: int | None = None,
        subcategory_id: int | None = None,
        amount: Decimal | None = None,
        transaction_date: date | None = None,
    ) -> Transaction:
        logger.info(f"Updating transaction with new amount: {amount}")

        if status_id is not None:
            status = self._ensure_status_belongs_to_user(
                status_id,
                _transaction.user_id,
            )
            if not status:
                raise TransactionUpdateError("Failed to update transaction")
            _transaction.status = status

        if subcategory_id is not None:
            subcategory = self._ensure_subcategory_belongs_to_user(
                subcategory_id,
                _transaction.user_id,
            )
            if not subcategory:
                raise TransactionUpdateError("Failed to update transaction")
            _transaction.subcategory = subcategory

        if amount is not None:
            _transaction.amount = amount

        if transaction_date is not None:
            _transaction.date = transaction_date

        _transaction.full_clean()
        _transaction.save()

        return _transaction

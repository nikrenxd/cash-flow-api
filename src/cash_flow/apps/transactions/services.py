import logging
from datetime import date
from decimal import Decimal

from django.db import transaction

from src.cash_flow.apps.transactions.models import Transaction

logger = logging.getLogger(__name__)


class TransactionService:
    @transaction.atomic
    def create_transaction(
        self,
        amount: Decimal,
        transaction_date: date,
        user_id: int,
    ) -> Transaction:
        logger.info(f"Creating new transaction for user with id: {user_id}")
        new_transaction = Transaction(
            amount=amount,
            date=transaction_date,
            user_id=user_id,
        )

        new_transaction.full_clean()
        new_transaction.save()

        return new_transaction

    @transaction.atomic
    def update_transaction(
        self,
        _transaction: Transaction,
        amount: Decimal,
        transaction_date: date | None = None,
    ) -> Transaction:
        logger.info(f"Updating transaction with new amount: {amount}")
        if transaction_date is not None:
            _transaction.date = transaction_date
        _transaction.amount = amount

        _transaction.full_clean()
        _transaction.save()

        return _transaction

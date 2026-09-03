from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class TransactionCreateDto:
    amount: Decimal
    user_id: int
    status_id: int
    subcategory_id: int
    transaction_date: date | None = None


@dataclass(frozen=True)
class TransactionUpdateDto:
    status_id: int | None = None
    subcategory_id: int | None = None
    amount: Decimal | None = None
    transaction_date: date | None = None

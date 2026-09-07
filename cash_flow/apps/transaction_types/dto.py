from dataclasses import dataclass


@dataclass(frozen=True)
class TransactionTypeCreateDto:
    name: str
    user_id: int | None = None
    description: str | None = None


@dataclass(frozen=True)
class TransactionTypeUpdateDto:
    name: str | None = None
    description: str | None = None

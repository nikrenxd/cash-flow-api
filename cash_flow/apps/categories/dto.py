from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCategoryDto:
    name: str
    transaction_type_id: int
    user_id: int


@dataclass(frozen=True)
class UpdateCategoryDto:
    transaction_type_id: int
    category_name: str | None = None

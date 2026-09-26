from dataclasses import dataclass


@dataclass(frozen=True)
class CreateSubcategoryDto:
    name: str
    user_id: int
    category_id: int


@dataclass(frozen=True)
class UpdateSubcategoryDto:
    name: str
    category_id: int

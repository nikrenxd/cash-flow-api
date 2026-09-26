from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCommentDto:
    user_id: int
    transaction_id: int
    body: str


@dataclass(frozen=True)
class UpdateCommentDto:
    body: str

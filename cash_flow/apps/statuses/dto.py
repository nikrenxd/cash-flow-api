from dataclasses import dataclass


@dataclass(frozen=True)
class CreateStatusDto:
    name: str
    user_id: int
    description: str | None = None


@dataclass(frozen=True)
class UpdateStatusDto:
    name: str | None = None
    description: str | None = None

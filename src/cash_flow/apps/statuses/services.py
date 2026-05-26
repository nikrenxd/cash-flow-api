from src.cash_flow.apps.statuses.models import Status


class StatusService:
    def create_status(
        self, name: str, user_id: int, description: str | None = None
    ) -> Status:
        new_status = Status(name=name, user_id=user_id, description=description)
        new_status.full_clean()
        new_status.save()

        return new_status

    def update_status(
        self,
        status: Status,
        name: str,
        description: str | None = None,
    ) -> Status:
        if description is not None:
            status.description = description
        status.name = name

        status.full_clean()
        status.save()

        return status

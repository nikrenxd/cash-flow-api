from django.db import transaction

from cash_flow.apps.statuses.dto import CreateStatusDto, UpdateStatusDto
from cash_flow.apps.statuses.models import Status


class StatusService:
    @transaction.atomic
    def create_status(self, data: CreateStatusDto) -> Status:
        new_status = Status(
            name=data.name,
            user_id=data.user_id,
            description=data.description,
        )
        new_status.full_clean()
        new_status.save()

        return new_status

    @transaction.atomic
    def update_status(self, status: Status, data: UpdateStatusDto) -> Status:
        if data.description is not None:
            status.description = data.description

        if data.name is not None:
            status.name = data.name

        status.full_clean()
        status.save()

        return status

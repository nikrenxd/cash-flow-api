from django.db.models import Q, QuerySet

from cash_flow.apps.statuses.exceptions import StatusObjectDoesNotExist
from cash_flow.apps.statuses.models import Status


class StatusSelector:
    def list_default_statuses(self, user_id: int) -> QuerySet[Status]:
        return Status.objects.filter(Q(user_id=None) | Q(user_id=user_id))

    def list_custom_statuses(self, user_id: int) -> QuerySet[Status] | None:
        return Status.objects.filter(user_id=user_id)

    def get_status_by_id(self, _id: int) -> Status:
        try:
            return Status.objects.get(id=_id)
        except Status.DoesNotExist:
            raise StatusObjectDoesNotExist

    def is_status_exists(self, user_id: int, status_id: int) -> bool:
        return Status.objects.filter(
            Q(id=status_id), Q(user_id=user_id) | Q(user_id=None)
        ).exists()

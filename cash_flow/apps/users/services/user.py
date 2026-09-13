import logging

from django.db import transaction

from cash_flow.apps.users.exceptions import (
    UserForActivationNotFound,
    UserIsAlreadyActive,
    UserObjectDoesNotExist,
)
from cash_flow.apps.users.models import CustomUser as User
from cash_flow.apps.users.selectors import UserSelector

logger = logging.getLogger(__name__)


class UserService:
    @transaction.atomic
    def create_user(self, email: str, password: str) -> User:
        user = User.objects.create_user(email=email, password=password)

        return user

    @transaction.atomic
    def update_user_active_status(self, user_id: int, token: str) -> User | None:
        try:
            user = UserSelector().get_activation_user_by_id(
                user_id=user_id,
                token=token,
            )
        except UserObjectDoesNotExist as e:
            logger.warning("User for activation was not found")
            raise UserForActivationNotFound from e

        if user.is_active:
            raise UserIsAlreadyActive

        user.is_active = True

        user.full_clean()
        user.save()

        return user

    def update_user_email_send(self, user: User) -> None:
        user.activation_email_send = True
        user.save()

    @transaction.atomic
    def delete_not_active_user(self, user_id: int) -> None:
        try:
            user = UserSelector().get_user_by_id_for_delete(id=user_id)
            if not user.is_active and user.activation_email_send:
                user.delete()
        except User.DoesNotExist as e:
            raise UserObjectDoesNotExist from e

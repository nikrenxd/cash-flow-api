import logging

from django.contrib.auth.tokens import default_token_generator
from django.db.models import QuerySet

from cash_flow.apps.users.exceptions import UserObjectDoesNotExist
from cash_flow.apps.users.models import CustomUser as User

logger = logging.getLogger(__name__)


class UserSelector:
    def list_users(self) -> QuerySet[User]:
        return User.objects.all()

    def get_user_by_id_for_delete(self, id: int) -> User:
        try:
            return User.objects.select_for_update().get(id=id)
        except User.DoesNotExist:
            raise UserObjectDoesNotExist

    def get_user_by_email(self, email: str) -> User | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise UserObjectDoesNotExist from e

    def get_activation_user_by_id(self, user_id: int, token: str) -> User | None:
        try:
            user = User.objects.get(id=user_id)

            if not default_token_generator.check_token(user, token):
                logger.warning(f"Invalid activation token for user: {user.id}")
                raise User.DoesNotExist

            return user

        except User.DoesNotExist as e:
            raise UserObjectDoesNotExist from e

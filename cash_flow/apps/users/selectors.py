import logging

from django.contrib.auth.tokens import default_token_generator
from django.db.models import QuerySet

from cash_flow.apps.users.exceptions import UserObjectDoesNotExist
from cash_flow.apps.users.models import CustomUser as User

logger = logging.getLogger(__name__)


class UserSelector:
    def list_users(self) -> QuerySet[User]:
        return User.objects.all()

    def get_user_by_email(self, email: str) -> User | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise UserObjectDoesNotExist from e

    def get_user_by_uuid(self, uuid: str, token: str) -> User | None:
        try:
            user = User.objects.select_related("email_id").get(
                email_id__email_uuid=uuid
            )
            if not default_token_generator.check_token(user, token):
                logger.warning(f"Invalid activation token for user: {user.id}")
                return None

            return user

        except User.DoesNotExist as e:
            raise UserObjectDoesNotExist from e

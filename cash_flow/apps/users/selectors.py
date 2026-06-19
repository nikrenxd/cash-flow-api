from django.db.models import QuerySet

from cash_flow.apps.users.exceptions import UserObjectDoesNotExist
from cash_flow.apps.users.models import CustomUser as User


class UserSelector:
    def list_users(self) -> QuerySet[User]:
        return User.objects.all()

    def get_user_by_email(self, email: str) -> User | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserObjectDoesNotExist

    def get_user_by_uidb(self, uidb64: str) -> User | None:
        try:
            return User.objects.get(pk=uidb64)
        except User.DoesNotExist:
            raise UserObjectDoesNotExist

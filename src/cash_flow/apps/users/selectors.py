from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode

from src.cash_flow.apps.users.exceptions import UserObjectDoesNotExist
from src.cash_flow.apps.users.models import CustomUser as User


class UserSelector:
    def list_users(self) -> QuerySet[User]:
        return User.objects.all()

    def get_user_by_email(self, email: str) -> User | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserObjectDoesNotExist
        # return get_object_or_404(User, email=email)

    def get_user_by_uidb(self, uidb64: str) -> User | None:
        try:
            return User.objects.get(pk=uidb64)
        except User.DoesNotExist:
            raise UserObjectDoesNotExist

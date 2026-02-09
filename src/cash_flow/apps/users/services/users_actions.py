from django.db import transaction

from src.cash_flow.apps.users.models import CustomUser as User


class UserService:
    @transaction.atomic
    def create_user(self, email: str, password: str) -> User:
        user = User.objects.create_user(email=email, password=password)

        return user

    @transaction.atomic
    def update_user_active_status(self, user: User) -> None:
        user.is_active = True

        user.full_clean()
        user.save()

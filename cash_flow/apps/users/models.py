import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from cash_flow.common.models import BaseModel


class CustomUserManager(BaseUserManager["CustomUser"]):
    def create_user(
        self, email: str, password: str | None = None, **extra_fields
    ) -> "CustomUser":
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields
    ) -> "CustomUser":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=155, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


class UserEmailId(BaseModel):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="email_id",
    )
    email_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
    )

    def __str__(self) -> str:
        return str(self.email_uuid)

    class Meta:
        db_table = "user_email_id"

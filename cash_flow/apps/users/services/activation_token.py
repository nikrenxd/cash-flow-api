import logging
import uuid

from django.conf import settings
from django.core.cache import cache

from cash_flow.apps.users.exceptions import UserActivationIdExpired

logger = logging.getLogger(__name__)


class ActivationTokenService:
    def set_email_id_token(self, user_id: int) -> uuid.UUID:
        email_id = uuid.uuid4()
        cache.set(
            key=f"{settings.ACTIVATION_EMAIL_ID_PREFIX}:{user_id}",
            value=email_id,
            timeout=int(settings.ACTIVATION_EMAIL_ID_TTL),
        )

        return email_id

    def set_activation_user_id(self, email_id: str, user_id: int) -> None:
        cache.set(
            key=f"{settings.ACTIVATION_EMAIL_ID_PREFIX}:{email_id}",
            value=user_id,
            timeout=int(settings.ACTIVATION_EMAIL_ID_TTL),
        )

    def retrieve_email_id_token(self, user_id: int) -> str | None:
        token_key = f"{settings.ACTIVATION_EMAIL_ID_PREFIX}:{user_id}"
        token = cache.get(key=token_key, default=None)

        if token:
            cache.delete(key=token_key)

        return token

    def retrieve_activation_user_id(self, email_id: str) -> int | None:
        key = f"{settings.ACTIVATION_EMAIL_ID_PREFIX}:{email_id}"
        user_id = cache.get(key=key, default=None)

        if not user_id:
            logger.error(f"User id with key: {key}:{email_id} is expired")
            raise UserActivationIdExpired(
                f"User id for email_id - {email_id}, expired"
            )

        cache.delete(key=key)

        return user_id

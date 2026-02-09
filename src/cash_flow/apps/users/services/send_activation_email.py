import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from src.cash_flow.apps.users.models import CustomUser as User
from src.cash_flow.common.send_email import send_email

logger = logging.getLogger(__name__)


def _prepare_confirmation_link(user: User) -> str:
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_path = reverse("activate", kwargs={"uidb64": uid, "token": token})
    return f"{settings.SITE_URL}{activation_path}"


def send_activation_email(user: User) -> None:
    confirmation_link = _prepare_confirmation_link(user)
    context = {
        "username": user.email,
        "confirmation_link": confirmation_link,
        "site_name": "cash-flow",
    }

    logger.info(f"Sending confirmation link to user {user.id}")
    send_email(
        email=user.email,
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject="Email activation link",
        context=context,
        template_name="email/activation_email.html",
    )
    logger.info(f"Confirmation email send successfully to user {user.id}")

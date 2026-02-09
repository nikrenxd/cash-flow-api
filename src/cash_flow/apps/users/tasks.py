import logging
from smtplib import SMTPException

from celery import shared_task
from django.http import Http404

from src.cash_flow.apps.users.exceptions import UserObjectDoesNotExist
from src.cash_flow.apps.users.selectors import UserSelector
from src.cash_flow.apps.users.services.send_activation_email import (
    send_activation_email,
)

logger = logging.getLogger(__name__)


@shared_task
def task_send_activation_email(email: str) -> None:
    try:
        user = UserSelector().get_user_by_email(email=email)
        send_activation_email(user=user)
    except (SMTPException, UserObjectDoesNotExist) as e:
        logger.error(f"Failed to send email from task: {e}")

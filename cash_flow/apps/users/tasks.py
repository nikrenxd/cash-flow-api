import logging
from smtplib import SMTPException

from celery import shared_task

from cash_flow.apps.users.exceptions import UserObjectDoesNotExist
from cash_flow.apps.users.selectors import UserSelector
from cash_flow.apps.users.services.activation_token import ActivationTokenService
from cash_flow.apps.users.services.send_activation_email import send_activation_email
from cash_flow.apps.users.services.user import UserService

logger = logging.getLogger(__name__)


@shared_task
def task_send_activation_email(email: str) -> None:
    try:
        user = UserSelector().get_user_by_email(email=email)
        if user is None:
            raise UserObjectDoesNotExist(f"User with email: {email} does not exist")

        email_id = ActivationTokenService().retrieve_email_id_token(user_id=user.id)
        if email_id is None:
            raise UserObjectDoesNotExist(
                f"Failed to get user activation token for user with email: {email}"
            )
        send_activation_email(
            user=user,
            email_id=email_id,
        )
        UserService().update_user_email_send(user=user)
    except (SMTPException, UserObjectDoesNotExist) as e:
        logger.warning(f"Failed to send email from task: {e}")


@shared_task
def task_delete_not_active_user(user_id: int) -> None:
    try:
        UserService().delete_not_active_user(user_id=user_id)
    except UserObjectDoesNotExist as e:
        logger.warning(f"Failed to delete user with expired activation time: {e}")

import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def _prepare_html_message(mail_context: dict, template_name: str) -> str:
    return render_to_string(template_name, mail_context)


def send_email(
    email: str,
    from_email: str,
    subject: str,
    context: dict,
    template_name: str,
):
    try:
        html_message = _prepare_html_message(
            mail_context=context,
            template_name=template_name,
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info("Email send successfully")
    except SMTPException as e:
        logger.error(f"Error while sending email: {e}")

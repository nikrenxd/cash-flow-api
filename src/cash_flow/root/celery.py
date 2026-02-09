import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.cash_flow.root.settings")

app = Celery("cash_flow")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

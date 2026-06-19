import os

CELERY = {
    "broker_url": os.environ.get(
        "CELERY_BROKER_URL",
        "amqp://guest:guest@localhost:5672//",
    ),
    "result_backend": os.environ.get(
        "CELERY_RESULT_BACKEND",
        "redis://localhost:6379",
    ),
}

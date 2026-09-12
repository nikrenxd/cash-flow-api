import os

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = bool(int(os.environ.get("EMAIL_USE_TLS")))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

ACTIVATION_EMAIL_ID_PREFIX = os.environ.get("ACTIVATION_EMAIL_ID_PREFIX")
ACTIVATION_EMAIL_ID_TTL = int(os.environ.get("ACTIVATION_EMAIL_ID_TTL"))

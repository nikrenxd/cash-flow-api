import os

from src.cash_flow.root.settings.components.base import INSTALLED_APPS, MIDDLEWARE

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-exg7*++as&o$o3$dh2yz3ce6s@xu9x3!u^muon*v+@g4n@wf&4"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
INTERNAL_IPS = ["127.0.0.1"]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = INSTALLED_APPS + [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False

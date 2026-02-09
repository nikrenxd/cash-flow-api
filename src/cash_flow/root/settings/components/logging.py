LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {name} {module} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "src.cash_flow.common": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "src.cash_flow.apps.users": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "src.cash_flow.apps.transactions": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

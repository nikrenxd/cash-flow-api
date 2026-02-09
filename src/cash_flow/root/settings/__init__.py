import os

import django_stubs_ext
from dotenv import load_dotenv
from split_settings.tools import include, optional  # noqa

load_dotenv()

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

# Managing environments via `DJANGO_ENV` variable:
ENV = os.environ.get("DJANGO_ENV", "development")

base_settings = (
    "components/base.py",
    "components/database.py",
    "components/cache.py",
    "components/celery.py",
    "components/auth.py",
    "components/drf.py",
    "components/email.py",
    "components/logging.py",
    # Select the right env:
    f"environments/{ENV}.py",
)

# Include settings:
include(*base_settings)

from collections.abc import Generator

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from cash_flow.apps.statuses.models import Status
from tests import constants
from tests.factories import (
    CommentFactory,
    CustomUserFactory,
    StatusFactory,
    TransactionFactory,
)

register(CustomUserFactory)
register(StatusFactory)
register(TransactionFactory)
register(CommentFactory)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authorized_client(api_client, custom_user) -> Generator[APIClient]:
    api_client.force_login(custom_user)
    yield api_client


@pytest.fixture
def default_status(status_factory) -> Status:
    return status_factory(
        name=constants.DEFAULT_STATUS,
        description=constants.DEFAULT_STATUS,
        user=None,
    )

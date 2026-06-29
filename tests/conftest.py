from typing import Generator

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from tests import constants
from tests.factories import CustomUserFactory, StatusFactory

register(CustomUserFactory)
register(StatusFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authorized_client(api_client, custom_user) -> Generator[APIClient]:
    api_client.force_login(custom_user)
    yield api_client


@pytest.fixture
def default_status(status_factory):
    return status_factory(
        name=constants.DEFAULT_STATUS,
        description=constants.DEFAULT_STATUS,
        user=None,
    )

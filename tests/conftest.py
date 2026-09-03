import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from cash_flow.apps.categories.models import Category
from cash_flow.apps.statuses.models import Status
from cash_flow.apps.transaction_types.models import TransactionType
from tests import constants
from tests.factories import (
    CategoryFactory,
    CommentFactory,
    CustomUserFactory,
    StatusFactory,
    SubcategoryFactory,
    TransactionFactory,
    TransactionTypeFactory,
)

register(CustomUserFactory)
register(StatusFactory)
register(TransactionFactory)
register(CommentFactory)
register(TransactionTypeFactory)
register(CategoryFactory)
register(SubcategoryFactory)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, custom_user) -> APIClient:
    api_client.force_login(custom_user)
    return api_client


@pytest.fixture
def other_authenticated_client(api_client, custom_user_factory) -> APIClient:
    user = custom_user_factory()
    api_client.force_login(user)
    return api_client


@pytest.fixture
def default_status(status_factory) -> Status:
    return status_factory(
        name=constants.DEFAULT_STATUS,
        description=constants.DEFAULT_STATUS,
        user=None,
    )


@pytest.fixture
def default_transaction_type(transaction_type_factory) -> TransactionType:
    return transaction_type_factory(
        name=constants.DEFAULT_TRANSACTION_TYPE,
        user=None,
    )


@pytest.fixture
def default_category(category_factory, default_transaction_type) -> Category:
    return category_factory(
        name=constants.DEFAULT_CATEGORY,
        transaction_type=default_transaction_type,
        user=None,
    )

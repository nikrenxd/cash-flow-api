import pytest
from django.db import IntegrityError

from cash_flow.apps.transaction_types.models import TransactionType
from tests.error_messages import NOT_NULL_ERR_MSG

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("parameter_name", ("name",))
def test_not_null_constraint(parameter_name: str, transaction_type_factory):
    relation_name = TransactionType._meta.db_table

    with pytest.raises(IntegrityError) as err:
        transaction_type_factory(**{parameter_name: None})

    assert NOT_NULL_ERR_MSG.format(
        column=parameter_name,
        relation=relation_name,
    ) in str(err.value), "Expected error message was not found"


def test_default_status(default_transaction_type):
    assert TransactionType.objects.filter(user=None).exists() is True
    assert default_transaction_type.user is None


def test_valid_creation(transaction_type: TransactionType):
    assert TransactionType.objects.count() == 1
    assert TransactionType.objects.get(id=transaction_type.id) == transaction_type

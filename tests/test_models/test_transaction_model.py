import pytest
from django.db import IntegrityError

from cash_flow.apps.transactions.models import Transaction
from tests.error_messages import NOT_NULL_ERR_MSG

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("parameter_name", ("amount", "user_id"))
def test_not_null_constraint(parameter_name: str, transaction_factory):
    relation_name = Transaction._meta.label_lower.replace(".", "_")

    with pytest.raises(IntegrityError) as err:
        transaction_factory(**{parameter_name: None})

    assert NOT_NULL_ERR_MSG.format(
        column=parameter_name,
        relation=relation_name,
    ) in str(err.value), "Expected error message was not found"


def test_valid_creation(transaction: Transaction):
    assert Transaction.objects.count() == 1
    assert Transaction.objects.get(id=transaction.id) == transaction

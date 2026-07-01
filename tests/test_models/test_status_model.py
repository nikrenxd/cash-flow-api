import pytest
from django.db import IntegrityError

from cash_flow.apps.statuses.models import Status
from tests.error_messages import NOT_NULL_ERR_MSG

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("parameter_name", ("name",))
def test_not_null_constraint(parameter_name: str, status_factory):
    relation_name = Status._meta.label_lower.replace(".", "_")

    with pytest.raises(IntegrityError) as err:
        status_factory(**{parameter_name: None})

    assert NOT_NULL_ERR_MSG.format(
        column=parameter_name,
        relation=relation_name,
    ) in str(err.value), "Expected error message was not found"


def test_default_status(default_status: Status):
    assert Status.objects.filter(user=None).exists() is True
    assert default_status.user is None


def test_valid_creation(status: Status):
    assert Status.objects.count() == 1
    assert Status.objects.get(id=status.id) == status

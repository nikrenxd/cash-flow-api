import pytest
from django.db import IntegrityError

from cash_flow.apps.users.models import CustomUser
from tests.error_messages import ALREADY_EXISTS_ERR_MSG, NOT_NULL_ERR_MSG

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "parameter_name",
    (
        "email",
        "password",
        "is_active",
        "is_staff",
        "date_joined",
    ),
)
def test_not_null_constraint(parameter_name: str, custom_user_factory):
    relation_name = CustomUser._meta.label_lower.replace(".", "_")

    with pytest.raises(IntegrityError) as err:
        custom_user_factory(**{parameter_name: None})

    assert NOT_NULL_ERR_MSG.format(
        column=parameter_name, relation=relation_name
    ) in str(err.value), "Expected error message was not found"


def test_valid_model(custom_user: CustomUser):
    assert CustomUser.objects.count() == 1
    assert CustomUser.objects.get(id=custom_user.id) == custom_user


def test_duplicate_user_not_allowed(custom_user: CustomUser, custom_user_factory):
    with pytest.raises(IntegrityError) as err:
        custom_user_factory(email=custom_user.email)

    assert ALREADY_EXISTS_ERR_MSG.format(
        column_name="email",
        column_value=custom_user.email,
    ) in str(err.value), "Expected error message was not found"

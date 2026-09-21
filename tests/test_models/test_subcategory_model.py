import pytest
from django.db import IntegrityError

from cash_flow.apps.subcategories.models import Subcategory
from tests.error_messages import NOT_NULL_ERR_MSG

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("parameter_name", ("name", "category_id"))
def test_not_null_constraint(parameter_name: str, subcategory_factory):
    relation_name = Subcategory._meta.db_table

    with pytest.raises(IntegrityError) as err:
        subcategory_factory(**{parameter_name: None})

    assert NOT_NULL_ERR_MSG.format(
        column=parameter_name,
        relation=relation_name,
    ) in str(err.value), "Expected error message was not found"


def test_valid_creation(subcategory: Subcategory):
    assert Subcategory.objects.count() == 1
    assert Subcategory.objects.get(id=subcategory.id) == subcategory

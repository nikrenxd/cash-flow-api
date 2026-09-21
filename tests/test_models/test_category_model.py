import pytest
from django.db import IntegrityError

from cash_flow.apps.categories.models import Category
from tests.error_messages import NOT_NULL_ERR_MSG

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("parameter_name", ("name", "transaction_type_id"))
def test_not_null_constraint(parameter_name: str, category_factory):
    relation_name = Category._meta.db_table

    with pytest.raises(IntegrityError) as err:
        category_factory(**{parameter_name: None})

    assert NOT_NULL_ERR_MSG.format(
        column=parameter_name,
        relation=relation_name,
    ) in str(err.value), "Expected error message was not found"


def test_valid_creation(category: Category):
    assert Category.objects.count() == 1
    assert Category.objects.get(id=category.id) == category


def test_default_category(default_category: Category):
    assert Category.objects.filter(id=default_category.id).exists() is True
    assert Category.objects.get(id=default_category.id) == default_category

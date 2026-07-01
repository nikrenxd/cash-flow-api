import pytest
from django.db import IntegrityError

from cash_flow.apps.comments.models import Comment
from tests.error_messages import NOT_NULL_ERR_MSG

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("parameter_name", ("body", "user_id", "transaction_id"))
def test_not_null_constraint(parameter_name: str, comment_factory):
    relation_name = Comment._meta.label_lower.replace(".", "_")

    with pytest.raises(IntegrityError) as err:
        comment_factory(**{parameter_name: None})

    assert NOT_NULL_ERR_MSG.format(
        column=parameter_name,
        relation=relation_name,
    ) in str(err.value), "Expected error message was not found"


def test_valid_creation(comment: Comment):
    assert Comment.objects.count() == 1
    assert Comment.objects.get(id=comment.id) == comment

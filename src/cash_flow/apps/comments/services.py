from django.db import transaction

from src.cash_flow.apps.comments.exceptions import CommentActionFailed
from src.cash_flow.apps.comments.models import Comment
from src.cash_flow.apps.transactions.selectors import TransactionSelector


class CommentService:
    @transaction.atomic
    def create_comment(
        self,
        user_id: int,
        transaction_id: int,
        body: str,
    ) -> Comment:
        is_transaction_exists = TransactionSelector().is_transaction_exists(
            transaction_id,
            user_id,
        )
        if not is_transaction_exists:
            raise CommentActionFailed

        new_comment = Comment(
            user_id=user_id,
            transaction_id=transaction_id,
            body=body,
        )
        new_comment.full_clean()
        new_comment.save()

        return new_comment

    @transaction.atomic
    def update_comment(self, comment: Comment, body: str) -> Comment:  # noqa: F821
        comment.body = body
        comment.full_clean()
        comment.save()

        return comment

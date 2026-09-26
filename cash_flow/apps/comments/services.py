from django.db import transaction

from cash_flow.apps.comments.dto import CreateCommentDto, UpdateCommentDto
from cash_flow.apps.comments.exceptions import CommentCreationError
from cash_flow.apps.comments.models import Comment
from cash_flow.apps.transactions.selectors import TransactionSelector


class CommentService:
    @transaction.atomic
    def create_comment(
        self,
        data: CreateCommentDto,
    ) -> Comment:
        is_transaction_exists = TransactionSelector().is_transaction_exists(
            data.transaction_id,
            data.user_id,
        )
        if not is_transaction_exists:
            raise CommentCreationError

        new_comment = Comment(
            user_id=data.user_id,
            transaction_id=data.transaction_id,
            body=data.body,
        )
        new_comment.full_clean()
        new_comment.save()

        return new_comment

    @transaction.atomic
    def update_comment(self, comment: Comment, data: UpdateCommentDto) -> Comment:
        comment.body = data.body
        comment.full_clean()
        comment.save()

        return comment

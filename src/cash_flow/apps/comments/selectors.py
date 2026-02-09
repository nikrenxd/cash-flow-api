from django.db.models import QuerySet

from src.cash_flow.apps.comments.exceptions import CommentObjectDoesNotExist
from src.cash_flow.apps.comments.models import Comment


class CommentSelector:
    def list_transaction_comments(
        self,
        user_id: int,
        transaction_id: int,
    ) -> QuerySet[Comment]:
        return Comment.objects.filter(user_id=user_id, transaction_id=transaction_id)

    def list_comments(self, user_id: int) -> QuerySet[Comment]:
        return Comment.objects.filter(user_id=user_id)

    def get_comment(self, comment_id: int) -> Comment | None:
        try:
            return Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise CommentObjectDoesNotExist

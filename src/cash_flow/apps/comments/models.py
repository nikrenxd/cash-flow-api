from django.db import models
from django.db.models import Index

from src.cash_flow.common.models import BaseModel


class Comment(BaseModel):
    body = models.TextField(max_length=300)
    user = models.ForeignKey(
        to="users.CustomUser",
        related_name="comments",
        on_delete=models.CASCADE,
    )
    transaction = models.ForeignKey(
        "transactions.Transaction",
        related_name="comments",
        on_delete=models.CASCADE,
    )

    class Meta:
        indexes = [Index(fields=["created_at"])]
        ordering = ["-created_at"]

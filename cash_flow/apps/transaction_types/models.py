from django.db import models

from cash_flow.common.models import BaseModel


class TransactionType(BaseModel):
    name = models.CharField(max_length=125, unique=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="transaction_types",
        null=True,
    )

    class Meta:
        db_table = "transaction_types"
        ordering = ("-created_at",)

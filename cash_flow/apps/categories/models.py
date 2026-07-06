from django.db import models

from cash_flow.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=125)

    transaction_type = models.ForeignKey(
        "transaction_types.TransactionType",
        on_delete=models.CASCADE,
        related_name="categories",
    )
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
    )

    class Meta:
        db_table = "categories"
        ordering = ("-created_at",)

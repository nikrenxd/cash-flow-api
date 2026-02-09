from django.db import models

from src.cash_flow.common.models import BaseModel


class Transaction(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(blank=True, null=True)

    user = models.ForeignKey(
        to="users.CustomUser",
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    def __str__(self):
        return f"Transaction with id: {self.id}; Amount: {self.amount};"

    class Meta:
        indexes = [
            models.Index(fields=["amount", "created_at"]),
        ]
        ordering = ["amount", "-created_at"]

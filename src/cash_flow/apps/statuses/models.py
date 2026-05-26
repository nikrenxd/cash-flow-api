from django.db import models

from src.cash_flow.common.models import BaseModel


class Status(BaseModel):
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=125, blank=True, null=True)
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="statuses",
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

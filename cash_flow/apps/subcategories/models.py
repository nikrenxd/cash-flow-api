from django.db import models

from cash_flow.common.models import BaseModel


class Subcategory(BaseModel):
    name = models.CharField(max_length=125)

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="subcategories",
    )

    class Meta:
        db_table = "subcategories"
        ordering = ("-created_at",)

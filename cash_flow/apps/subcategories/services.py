from django.db import transaction

from cash_flow.apps.subcategories.dto import (
    CreateSubcategoryDto,
    UpdateSubcategoryDto,
)
from cash_flow.apps.subcategories.models import Subcategory


class SubcategoryService:
    @transaction.atomic
    def create_subcategory(self, data: CreateSubcategoryDto) -> Subcategory:
        new_subcategory = Subcategory(
            name=data.name,
            user_id=data.user_id,
            category_id=data.category_id,
        )

        new_subcategory.full_clean()
        new_subcategory.save()

        return new_subcategory

    @transaction.atomic
    def update_subcategory(
        self,
        subcategory: Subcategory,
        data: UpdateSubcategoryDto,
    ) -> Subcategory:
        subcategory.name = data.name
        subcategory.category_id = data.category_id

        subcategory.full_clean()
        subcategory.save()

        return subcategory

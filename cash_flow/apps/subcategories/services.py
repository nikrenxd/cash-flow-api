from django.db import transaction

from cash_flow.apps.subcategories.models import Subcategory


class SubcategoryService:
    @transaction.atomic
    def create(
        self, subcategory_name: str, user_id: int, category_id: int
    ) -> Subcategory:
        new_subcategory = Subcategory(
            name=subcategory_name,
            user_id=user_id,
            category_id=category_id,
        )

        new_subcategory.full_clean()
        new_subcategory.save()

        return new_subcategory

    @transaction.atomic
    def update(
        self,
        subcategory: Subcategory,
        subcategory_name: str,
        category_id: int,
    ) -> Subcategory:
        subcategory.name = subcategory_name
        subcategory.category_id = category_id

        subcategory.full_clean()
        subcategory.save()

        return subcategory

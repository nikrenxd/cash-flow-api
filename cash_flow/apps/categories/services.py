from django.db import transaction

from cash_flow.apps.categories.models import Category


class CategoryService:
    @transaction.atomic
    def create_category(
        self,
        category_name: str,
        transaction_type_id: int,
        user_id: int,
    ) -> Category:
        new_category = Category(
            name=category_name,
            transaction_type_id=transaction_type_id,
            user_id=user_id,
        )

        new_category.full_clean()
        new_category.save()

        return new_category

    @transaction.atomic
    def update_category(
        self,
        category: Category,
        transaction_type_id: int,
        category_name: str | None = None,
    ) -> Category:
        category.transaction_type_id = transaction_type_id

        if category_name is not None:
            category.name = category_name

        category.full_clean()
        category.save()

        return category

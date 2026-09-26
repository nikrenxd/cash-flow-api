from django.db import transaction

from cash_flow.apps.categories.dto import CreateCategoryDto, UpdateCategoryDto
from cash_flow.apps.categories.models import Category


class CategoryService:
    @transaction.atomic
    def create_category(
        self,
        data: CreateCategoryDto,
    ) -> Category:
        new_category = Category(
            name=data.name,
            transaction_type_id=data.transaction_type_id,
            user_id=data.user_id,
        )

        new_category.full_clean()
        new_category.save()

        return new_category

    @transaction.atomic
    def update_category(
        self,
        category: Category,
        data: UpdateCategoryDto,
    ) -> Category:
        category.transaction_type_id = data.transaction_type_id

        if data.category_name is not None:
            category.name = data.category_name

        category.full_clean()
        category.save()

        return category

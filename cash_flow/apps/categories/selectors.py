from django.db.models import Q, QuerySet

from cash_flow.apps.categories.exceptions import CategoryObjectDoesNotExist
from cash_flow.apps.categories.models import Category


class CategorySelector:
    def none_category(self) -> None:
        return Category.objects.none()

    def list_categories(
        self, user_id: int, transaction_type_id: int
    ) -> QuerySet[Category]:
        return Category.objects.select_related("transaction_type").filter(
            Q(user_id=None) | Q(user_id=user_id),
            transaction_type_id=transaction_type_id,
        )

    def get_category(self, category_id: int, user_id: int) -> Category:
        try:
            return Category.objects.get(id=category_id, user_id=user_id)
        except Category.DoesNotExist as e:
            raise CategoryObjectDoesNotExist from e

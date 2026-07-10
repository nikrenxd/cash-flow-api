from django.db.models import QuerySet

from cash_flow.apps.subcategories.models import Subcategory


class SubcategorySelector:
    def list_subcategories(
        self, user_id: int, category_id: int
    ) -> QuerySet[Subcategory]:
        return Subcategory.objects.filter(user_id=user_id, category_id=category_id)

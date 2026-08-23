from django.db.models import QuerySet

from cash_flow.apps.subcategories.exceptions import SubcategoryObjectDoesNotExist
from cash_flow.apps.subcategories.models import Subcategory


class SubcategorySelector:
    def list_subcategories(
        self, user_id: int, category_id: int
    ) -> QuerySet[Subcategory]:
        return Subcategory.objects.select_related("category").filter(
            user_id=user_id,
            category_id=category_id,
        )

    def get_subcategory_by_id(self, _id: int) -> Subcategory:
        try:
            return Subcategory.objects.get(id=_id)
        except Subcategory.DoesNotExist as e:
            raise SubcategoryObjectDoesNotExist from e

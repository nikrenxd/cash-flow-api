from rest_framework import permissions
from rest_framework.exceptions import NotFound

from cash_flow.apps.categories.exceptions import CategoryObjectDoesNotExist
from cash_flow.apps.categories.selectors import CategorySelector


class IsCategoryBelongsToUser(permissions.BasePermission):
    def has_permission(self, request, view):
        category_id = view.kwargs.get("category_id")
        if category_id is None:
            return False

        try:
            category = CategorySelector().get_category(
                category_id=category_id,
                user_id=request.user.id,
            )

            return category.user.id == request.user.id
        except CategoryObjectDoesNotExist as e:
            raise NotFound from e

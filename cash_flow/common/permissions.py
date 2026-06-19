from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        return obj.user == request.user

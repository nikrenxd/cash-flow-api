from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        return obj.user == request.user


class IsOwnerOrDefaultObjectPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        # if default object
        if obj.user is None and request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

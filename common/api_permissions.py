from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from typing import List
from .cons import PERMISSION_METHOD


# class HasPermissionKeycloakCustom(BasePermission):
#     def has_permission(self, request, view):
#         user_permissions: List[str] = request.auth['realm_access']['roles']
#         user = request.user if request.user else None
#         obj = ContentType.objects.get_for_model(view.queryset.model)
#         permission = PERMISSION_METHOD[request.method] + obj.model.upper()
#         return user and permission in user_permissions

# class CanAdd(BasePermission):
#     def has_permission(self, request, view):
#         user_permissions: List[str] = request.auth['realm_access']['roles']
#         user = request.user if request.user else None
#         obj = ContentType.objects.get_for_model(view.queryset.model)
#         permission = 'add_' + obj.model
#         return user and permission in user_permissions
#
#
# class CanChange(BasePermission):
#     def has_permission(self, request, view):
#         user_permissions: List[str] = request.auth['realm_access']['roles']
#         user = request.user if request.user else None
#         obj = ContentType.objects.get_for_model(view.queryset.model)
#         permission = 'change_' + obj.model
#         return user and permission in user_permissions
#
#
# class CanDelete(BasePermission):
#     def has_permission(self, request, view):
#         user_permissions: List[str] = request.auth['realm_access']['roles']
#         user = request.user if request.user else None
#         obj = ContentType.objects.get_for_model(view.queryset.model)
#         permission = 'delete_' + obj.model
#         return user and permission in user_permissions

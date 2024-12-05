from rest_framework.permissions import BasePermission

class IsPropertyManager(BasePermission):
    """
    Allows access only to users with the role of 'Property Manager'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "Property Manager"

class IsTenant(BasePermission):
    """
    Allows access only to users with the role of 'Tenant'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "Tenant"
from rest_framework.permissions import BasePermission

class IsPropertyManager(BasePermission):
    """
    Custom permission to allow only property managers to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.role == "Property Manager"
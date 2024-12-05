from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from shared.permissions import IsPropertyManager
from .models import Tenant
from .serializers import TenantSerializer

class TenantListCreateView(ListCreateAPIView):
    """
    Allows Property Managers to list and create tenants.
    """
    permission_classes = [IsAuthenticated, IsPropertyManager]
    serializer_class = TenantSerializer

    def get_queryset(self):
        # Optimize by fetching related property and user in a single query
        return (
            Tenant.objects.filter(assigned_property__managers=self.request.user)
            .select_related("user", "assigned_property")
        )

    def perform_create(self, serializer):
        # Automatically associate the tenant with the current user
        serializer.save()


class TenantDetailView(RetrieveUpdateDestroyAPIView):
    """
    Allows Property Managers to retrieve, update, or delete tenant details.
    """
    permission_classes = [IsAuthenticated, IsPropertyManager]
    serializer_class = TenantSerializer

    def get_queryset(self):
        # Apply the same optimization for detail view
        return (
            Tenant.objects.filter(created_by=self.request.user)
            .select_related("user", "assigned_property")
        )
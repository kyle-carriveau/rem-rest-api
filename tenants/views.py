from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from shared.permissions import IsPropertyManager
from .models import Tenant
from .serializers import TenantSerializer

class TenantListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsPropertyManager]
    serializer_class = TenantSerializer

    def get_queryset(self):
        # Filter tenants by the current user
        return Tenant.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the tenant with the current user
        serializer.save(created_by=self.request.user)

class TenantDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TenantSerializer

    def get_queryset(self):
        # Filter tenants by the current user
        return Tenant.objects.filter(created_by=self.request.user)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsPropertyManager
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lease
from .serializers import LeaseSerializer
from .filters import LeaseFilter

class LeaseListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsPropertyManager]
    serializer_class = LeaseSerializer
    filter_backends = [DjangoFilterBackend] # Add filter backend
    filterset_class = LeaseFilter # Add the filterset

    def get_queryset(self):
        # Restrict to leases associated with properties managed by the current user
        # Optimize with select_related for foreign keys and prefetch_related for many-to-many relationships
        return (
            Lease.objects.filter(property__managers=self.request.user)
            .select_related("property", "tenant")
            .prefetch_related("property__tenants") # Optimize reverse relationship from Property to Tenants
        )

class LeaseDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsPropertyManager]
    serializer_class = LeaseSerializer

    def get_queryset(self):
        return (
            Lease.objects.filter(property__managers=self.request.user)
            .select_related("property", "tenant")
            .prefetch_related("property__tenants")
        )
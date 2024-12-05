from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from authentication.permissions import IsPropertyManager, IsTenant

class PaymentListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTenant]  # Restrict to Tenants
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["payment_date", "amount"]  # Example filters
    ordering_fields = ["payment_date", "amount"]

    def get_queryset(self):
        return Payment.objects.filter(tenant=self.request.user)

class PaymentListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]  # Add filter backend
    filterset_class = PaymentFilter  # Add the filterset
    search_fields = ["tenant__first_name", "tenant__last_name"]  # Search by tenant name
    ordering_fields = ["payment_date", "amount"]  # Order by date or amount

    def get_queryset(self):
        # Optimize related queries for lease and tenant relationships
        return (
            Payment.objects.filter(lease__property__created_by=self.request.user)
            .select_related("lease", "tenant")  # Optimize foreign key relationships
            .prefetch_related("lease__property")  # Prefetch related property for lease
        )

class PaymentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        # Apply the same optimization for detail view
        return (
            Payment.objects.filter(lease__property__created_by=self.request.user)
            .select_related("lease", "tenant")  # Optimize foreign key relationships
            .prefetch_related("lease__property")  # Prefetch related property for lease
        )
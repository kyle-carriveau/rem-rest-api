from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Lease
from .serializers import LeaseSerializer

class LeaseListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaseSerializer

    def get_queryset(self):
        # Restrict to leases associated with properties managed by the current user
        return Lease.objects.filter(property__created_by=self.request.user)

class LeaseDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaseSerializer

    def get_queryset(self):
        return Lease.objects.filter(property__created_by=self.request.user)
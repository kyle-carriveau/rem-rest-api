from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer

class PaymentListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        # Restrict payments to those associated with properties managed by the user
        return Payment.objects.filter(lease__property__created_by=self.request.user)

class PaymentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(lease__property__created_by=self.request.user)
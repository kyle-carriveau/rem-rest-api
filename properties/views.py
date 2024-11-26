from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Property
from .serializers import PropertySerializer

class PropertyListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer

    def get_queryset(self):
        return (
            Property.objects.filter(created_by=self.request.user)
                .select_related("owner")
                .prefetch_related("tenants")
        )
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PropertyDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer

    def get_queryset(self):
        return (
            Property.objects.filter(created_by=self.request.user)
            .select_related("owner")
            .prefetch_related("tenants")
        )
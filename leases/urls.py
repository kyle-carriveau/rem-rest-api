from django.urls import path
from .views import LeaseListCreateView, LeaseDetailView

urlpatterns = [
    path("", LeaseListCreateView.as_view(), name="lease-list-create"),
    path("<int:pk>/", LeaseDetailView.as_view(), name="lease-detail"),
]
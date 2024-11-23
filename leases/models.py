from django.db import models
from properties.models import Property
from tenants.models import Tenant

class Lease(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="leases")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="leases")
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Expired", "Expired"), ("Terminated", "Terminated")],
        default="Active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lease for {self.tenant} at {self.property} ({self.start_date} - {self.end_date})"
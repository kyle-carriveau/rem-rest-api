from django.db import models
from properties.models import Property
from tenants.models import Tenant
from django.db.models import Sum
from django.utils import timezone

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
    
    def update_status(self):
        total_payments = self.payments.aggregate(Sum("amount"))["amount__sum"] or 0
        if total_payments >= self.rent_amount:
            self.status = "Paid in Full"
        elif self.end_date < timezone.now().date():
            self.status = "Expired"
        else:
            self.status = "Active"
        self.save()

    class Meta:
        constraints = [
            # Ensure start_date is less than end_date
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F("end_date")),
                name="start_date_before_end_date"
            ),
            # Ensure no overlapping leases for the same tenant and property
            models.UniqueConstraint(
                fields=["tenant", "property", "start_date", "end_date"],
                name="unique_lease_per_tenant"
            ),
        ]
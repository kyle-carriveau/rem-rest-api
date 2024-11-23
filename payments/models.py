from django.db import models
from leases.models import Lease
from tenants.models import Tenant

class Payment(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name="payments")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=50,
        choices=[("Credit Card", "Credit Card"), ("Cash", "Cash"), ("Bank Transfer", "Bank Transfer")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant} on {self.payment_date}"
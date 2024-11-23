from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from properties.models import Property
from tenants.models import Tenant
from leases.models import Lease
from payments.models import Payment

User = get_user_model()

class PaymentAPITest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager", password="password123", role="Property Manager"
        )
        self.property = Property.objects.create(
            name="Test Property", address="123 Main St", units=10, type="Residential", created_by=self.manager
        )
        self.tenant = Tenant.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com", assigned_property=self.property, created_by=self.manager
        )
        self.lease = Lease.objects.create(
            property=self.property, tenant=self.tenant, start_date="2024-01-01", end_date="2024-12-31", rent_amount="1500.00", status="Active"
        )
        self.payment = Payment.objects.create(
            lease=self.lease, tenant=self.tenant, amount="1500.00", payment_date="2024-11-20", payment_method="Bank Transfer"
        )
        self.client = APIClient()

    def test_list_payments(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get("/api/payments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_payment(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(
            "/api/payments/",
            {
                "lease": self.lease.id,
                "tenant": self.tenant.id,
                "amount": "1500.00",
                "payment_date": "2024-11-21",
                "payment_method": "Cash"
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_delete_payment(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.delete(f"/api/payments/{self.payment.id}/")
        self.assertEqual(response.status_code, 204)
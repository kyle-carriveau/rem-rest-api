from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from properties.models import Property
from tenants.models import Tenant
from leases.models import Lease

User = get_user_model()

class LeaseAPITest(TestCase):
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

        self.client = APIClient()

    def test_manager_can_create_lease(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(
            "/api/leases/",
            {
                "property": self.property.id,
                "tenant": self.tenant.id,
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "rent_amount": "1500.00",
                "status": "Active"
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_manager_can_list_leases(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get("/api/leases/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
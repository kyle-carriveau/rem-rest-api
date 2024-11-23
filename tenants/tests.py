from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from properties.models import Property
from tenants.models import Tenant

User = get_user_model()

class TenantAPITest(TestCase):
    def setUp(self):
        # Create a property manager
        self.manager = User.objects.create_user(
            username="manager", password="password123", role="Property Manager"
        )

        # Create a tenant user
        self.tenant_user = User.objects.create_user(
            username="tenant", password="password123", role="Tenant"
        )

        # Create a property
        self.property = Property.objects.create(
            name="Test Property", address="123 Main St", units=10, type="Residential", created_by=self.manager
        )

        # Create API client
        self.client = APIClient()

    def test_property_manager_can_create_tenant(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(
            "/api/tenants/",
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "assigned_property": self.property.id,
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_tenant_cannot_create_tenant(self):
        self.client.force_authenticate(user=self.tenant_user)
        response = self.client.post(
            "/api/tenants/",
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "assigned_property": self.property.id,
            },
        )
        self.assertEqual(response.status_code, 403)
from rest_framework.test import APITestCase
from authentication.models import User
from properties.models import Property
from tenants.models import Tenant
from payments.models import Payment

class PropertyManagerAccessTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username="manager", role="Property Manager", password="password")
        self.other_manager = User.objects.create_user(username="other_manager", role="Property Manager", password="password")
        self.property = Property.objects.create(name="Test Property", created_by=self.manager)

    def test_manager_access(self):
        self.client.login(username="manager", password="password")
        response = self.client.get("/api/properties/")
        self.assertEqual(response.status_code, 200)  # Manager should have access

    def test_other_manager_access_denied(self):
        self.client.login(username="other_manager", password="password")
        response = self.client.get(f"/api/properties/{self.property.id}/")
        self.assertEqual(response.status_code, 403)  # Access denied to unrelated properties

class TenantAccessTests(APITestCase):
    def setUp(self):
        self.tenant = User.objects.create_user(username="tenant", role="Tenant", password="password")
        self.other_tenant = User.objects.create_user(username="other_tenant", role="Tenant", password="password")
        self.payment = Payment.objects.create(tenant=self.tenant, amount=100)

    def test_tenant_access(self):
        self.client.login(username="tenant", password="password")
        response = self.client.get("/api/payments/")
        self.assertEqual(response.status_code, 200)  # Tenant should have access to their payments

    def test_other_tenant_access_denied(self):
        self.client.login(username="other_tenant", password="password")
        response = self.client.get(f"/api/payments/{self.payment.id}/")
        self.assertEqual(response.status_code, 403)  # Access denied to other tenants' payments
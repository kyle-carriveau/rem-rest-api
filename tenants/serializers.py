from rest_framework import serializers
from tenants.models import Tenant
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "phone_number"]

class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Tenant
        fields = "__all__"

    def validate(self, data):
        if Tenant.objects.filter(
            email=data["email"],
            assigned_property=data["assigned_property"],
        ).exists():
            raise serializers.ValidationError("This tenant is already assigned to this property.")
        return data
        
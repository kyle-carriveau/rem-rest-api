from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from tenants.models import Tenant

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role", "phone_number"]
        read_only_fields = ["role"]

    def validate_role(self, value):
        if value not in dict(CustomUser.ROLE_CHOICES):
            raise serializers.ValidationError("Invalid role.")
        return value
    
    def validate_email(self, value):
        if Tenant.objects.filter(email=value).exists():
            raise serializers.ValidationError("A tenant with this email already exists.")
        return value

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if value and len(value) not in [10, 15]:
            raise serializers.ValidationError("Phone number must be 10-15 digits long.")
        return value
    
    def create(self, validated_data):
        return super().create(validated_data)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()  # Blacklist the token if using token blacklisting
        except AttributeError:
            raise serializers.ValidationError("Token blacklisting is not enabled.")
        except Exception as e:
            raise serializers.ValidationError(f"An error ocurred during logout: {str(e)}")
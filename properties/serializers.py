from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"

    def validate_units(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of units must be greater than 0.")
        return value

    def validate(self, data):
        user = self.context["request"].user
        if Property.objects.filter(name=data["name"], address=data["address"], created_by=user).exists():
            raise serializers.ValidationError("A property with this name and address already exists.")
        if len(data.get("name", "")) > 100:
            raise serializers.ValidationError("Property name must not exceed 100 characters.")
        return data
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "is_late", "lease_status")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be greater than 0.")
        return value
    
    def validate(self, data):
        lease = data.get("lease")
        payment_date = data.get("payment_date")

        if lease and payment_date > lease.end_date:
            data["is_late"] = True
        else:
            data["is_late"] = False

        return data
    
    
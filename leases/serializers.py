from rest_framework import serializers
from .models import Lease
from django.utils.timezone import now

class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = "__all__"
       
    def validate(self, data):
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date.")
        if data["rent_amount"] <= 0:
            raise serializers.ValidationError("Rent amount must be positive.")
        return data
    
    def save(self, *args, **kwargs):
        if self.end_date < now().date():
            self.status = "Expired"
        if self.start_date > now().date():
            self.status = "Upcoming"
        if self.start_date < now().date() and self.end_date > now().date():
            self.status = "Active"
        super().save(*args, **kwargs)
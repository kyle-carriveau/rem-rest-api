from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("lease", "tenant", "amount", "payment_date", "payment_method", "created_at")
    list_filter = ("payment_method", "payment_date")
    search_fields = ("tenant__first_name", "tenant__last_name", "lease__property__name")
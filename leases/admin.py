from django.contrib import admin
from .models import Lease

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ("property", "tenant", "start_date", "end_date", "rent_amount", "status", "created_at")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("property__name", "tenant__first_name", "tenant__last_name")
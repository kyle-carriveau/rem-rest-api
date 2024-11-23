from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "assigned_property", "created_by", "created_at")
    search_fields = ("first_name", "last_name", "email", "assigned_property__name")
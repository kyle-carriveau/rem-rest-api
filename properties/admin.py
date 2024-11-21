from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "type", "units", "created_by", "created_at")
    search_fields = ("name", "address")
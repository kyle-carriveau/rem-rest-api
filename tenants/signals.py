from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from tenants.models import Tenant

@receiver(post_save, sender=User)
def create_tenant_profile(sender, instance, created, **kwargs):
    if created and instance.role == "Tenant":
        Tenant.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_tenant_profile(sender, instance, **kwargs):
    if instance.role == "Tenant" and hasattr(instance, 'tenant_profile'):
        instance.tenant_profile.save()
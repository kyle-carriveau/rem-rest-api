from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment

@receiver(post_save, sender=Payment)
def update_lease_status(sender, instance, **kwargs):
    lease = instance.lease
    lease.update_status()  
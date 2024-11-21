from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    units = models.IntegerField()
    type = models.CharField(
        max_length=50,
        choices=[("Residential", "Residential"), ("Commercial", "Commercial")],
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
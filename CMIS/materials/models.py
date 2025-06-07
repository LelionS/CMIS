import uuid
from django.db import models
from decimal import Decimal

class MaterialCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Material(models.Model):
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)
    supplier = models.CharField(max_length=100)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    delivery_date = models.DateField()
    batch_code = models.CharField(max_length=50, unique=True, blank=True)
    amount_in_stock = models.IntegerField()
    image = models.ImageField(upload_to='materials/', blank=True, null=True)

    is_available = models.BooleanField(default=True) 

    def generate_unique_batch_code(self):
        from django.utils.text import slugify
        while True:
            code = f"BATCH-{uuid.uuid4().hex[:8].upper()}"
            if not Material.objects.filter(batch_code=code).exists():
                return code
                
    def save(self, *args, **kwargs):
        if self.amount_in_stock <= 0:
            self.is_available = False
        super(Material, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.batch_code:
            self.batch_code = self.generate_unique_batch_code()
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class MaterialRequest(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requests')
    request_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    status_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='status_updates')
    status_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.material.name} ({self.status})"

from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('apparel', 'Apparel'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('others', 'Others'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='EQUIPMENT')
    is_featured = models.BooleanField(default=False)
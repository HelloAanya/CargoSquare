from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100)
    specification = models.TextField()
    quantity = models.IntegerField()  # Add the quantity field
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('collected', 'Collected'),
        ('pending', 'Pending')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} ({self.status})"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"
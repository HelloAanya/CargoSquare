from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100)
    specification = models.TextField()
    quantity = models.IntegerField()  
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('collected', 'Collected')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    
    def __str__(self):
        return f"Order {self.id} ({self.status})"

class OrderLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.id}: {self.name}"


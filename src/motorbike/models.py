from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
TRANSPORT_CHOICES = [
    ('bodaboda', 'Bodaboda Rider'),
    ('pickup', 'Pickup Driver'),
    ('lorry', 'Lorry Driver'),
]

class Driver(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    number_plate = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    sacco = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)
    county = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='drivers/', default='default_driver.png')
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
class Booking(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.driver.full_name}"

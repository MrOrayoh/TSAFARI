from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class DriverManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Driver(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    # Assuming TRANSPORT_CHOICES might still be relevant for the 'role' field,
    # you might want to redefine it or pass choices directly to the field.
    # For now, role is a simple CharField as per your provided snippet.
    TRANSPORT_CHOICES = [
        ('bodaboda', 'Bodaboda Rider'),
        ('pickup', 'Pickup Driver'),
        ('lorry', 'Lorry Driver'),
    ]
    role = models.CharField(max_length=20, choices=TRANSPORT_CHOICES, blank=True) # Added choices and blank=True
    number_plate = models.CharField(max_length=20, blank=True)
    sacco = models.CharField(max_length=100, blank=True) # Increased max_length to match previous, added blank=True
    stage = models.CharField(max_length=100, blank=True) # Increased max_length to match previous, added blank=True
    county = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='drivers/', default='default_driver.png', blank=True, null=True) # Matched previous upload_to and default

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # is_staff is needed for admin login

    objects = DriverManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone'] # These fields will be prompted for when creating a superuser

    def __str__(self):
        return self.email

    # Add related_name to avoid clashes with default User model's reverse accessors
    # if you were to use both in the same project (unlikely with AUTH_USER_MODEL set)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="driver_set", # Changed related_name
        related_query_name="driver",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="driver_set", # Changed related_name
        related_query_name="driver",
    )

class Booking(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.driver.full_name}"
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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

    TRANSPORT_CHOICES = [
        ('bodaboda', 'Boda Boda'),
        ('pickup', 'Pickup'),
        ('lorry', 'Lorry'),
    ]
    role = models.CharField(max_length=50, choices=TRANSPORT_CHOICES, blank=True)
    number_plate = models.CharField(max_length=20, blank=True)
    sacco = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=50, blank=True)

    rating = models.FloatField(default=4.5)
    photo = models.ImageField(upload_to='driver_photos/', null=True, blank=True)
    is_available = models.BooleanField(default=False)

    profile_picture = models.ImageField(upload_to='drivers/', default='default_driver.png', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = DriverManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    def __str__(self):
        return self.email

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return ''

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="driver_set",
        related_query_name="driver",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="driver_set",
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

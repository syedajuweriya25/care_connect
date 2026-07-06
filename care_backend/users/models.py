from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('resident', 'Resident'),
        ('guardian', 'Guardian'),
        ('volunteer', 'Volunteer'),
        ('security', 'Security'),
        ('admin', 'Admin'),
    ]

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')
    blood_group = models.CharField(max_length=10, blank=True)
    emergency_contact_name = models.CharField(max_length=120, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    medical_conditions = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    role_details = models.JSONField(blank=True, null=True, default=dict)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.email

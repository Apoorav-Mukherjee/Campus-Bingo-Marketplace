from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """
    Custom User model for Bingo Campus Marketplace.
    Extends AbstractUser to add student-specific fields.
    """
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    # College/department info
    college_name = models.CharField(max_length=150, blank=True, null=True)
    graduation_year = models.PositiveIntegerField(blank=True, null=True)

    # Use email as the unique identifier for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    google_id = models.CharField(max_length=255, null=True, blank=True)
    sign_up_method = models.CharField(max_length=50, default='google')

    # Ensure username is not blank
    username = models.CharField(max_length=150, unique=False, null=False, blank=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.email})"

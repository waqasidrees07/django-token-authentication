from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator


class User(AbstractUser):
    """Model to create User"""
    username = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=40, unique=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        """username"""
        return self.email

    def get_full_name(self):
        """Return the full name of the user."""
        return self.full_name


class ResetCode(models.Model):
    """ Code To Maintain User Reset Codes """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=6, validators=[MinLengthValidator(4), MaxLengthValidator(4)])
    updated_at = models.DateTimeField(auto_now=True)
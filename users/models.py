"""
Importações do Django
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfileExample(models.Model):
    """
    Model de Users
    """
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=150)
    birth_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        """
        Nomes de Users
        """
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

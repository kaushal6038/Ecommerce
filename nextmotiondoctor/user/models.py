from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import PermissionsMixin


class CustomUser(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=7, default='Doctor', editable=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return str(self.email)

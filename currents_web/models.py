from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager

# Login details
class User(AbstractBaseUser, PermissionsMixin):
       email = models.EmailField(primary_key=True)
       password = models.CharField(max_length=20)
       
       is_staff = models.BooleanField(default=True)
       is_superuser = models.BooleanField(default=False)
       last_login = None

       objects = UserManager()

       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = []
       
       def get_full_name(self):
              return self.username
       
       def __str__(self):
              return self.email

# user details
class UserDetails(models.Model):
       email = models.ForeignKey(User, to_field="email", on_delete=models.CASCADE, primary_key=True)
       username = models.CharField(max_length=20)
       userPreferences = models.CharField(max_length=300)
       
       def __str__(self):
              return self.username


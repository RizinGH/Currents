from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager

# Login details
class User(AbstractBaseUser, PermissionsMixin):
       email = models.EmailField(
              primary_key=True
       )
       password = models.CharField(
              max_length=20
       )
       
       is_staff = models.BooleanField(
              default=True
       )
       is_superuser = models.BooleanField(
              default=False
       )
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
       user = models.OneToOneField(
              User, 
              to_field="email", 
              on_delete=models.CASCADE, 
              primary_key=True
       )
       username = models.CharField(
              max_length=20
       )
       userPreferences = models.CharField(
              max_length=300
       )
       
       def __str__(self):
              return self.username

# subscription details
class Subscription(models.Model):
       user = models.OneToOneField(
              User,
              to_field='email',
              primary_key=True,
              on_delete=models.CASCADE
       )
       date = models.DateField(
              null=False
       )
       amount = models.IntegerField(
              null=False
       )
       payment_mode = models.CharField(
              null=False,
              max_length=10
       )

# saved articles
class Favourites(models.Model):
       id = models.AutoField(
              primary_key=True
       )

       user = models.ForeignKey(
              User,
              to_field='email',
              on_delete=models.CASCADE
       )

       title = models.CharField(
              max_length=100,
              null=False
       )

       url = models.CharField(
              null=False,
              max_length=500
       )

# report
class Report(models.Model):
       id = models.AutoField(
              primary_key=True
       )

       date = models.DateField(
              null=False
       )

       total_users = models.IntegerField(
              null=False
       )

       total_subscribers = models.IntegerField(
              null=False
       )
from django.db import models

class Login(models.Model):
     email = models.EmailField()
     password = models.CharField(max_length=20)
     def __str__(self):
            return self.headline

class UserDetails(models.Model):
        username = models.CharField(max_length=20)
        email = models.EmailField()
        password = models.CharField(max_length=20)
        def __str__(self):
               return self.headline


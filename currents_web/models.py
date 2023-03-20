from django.db import models

class Login(models.Model):
       email = models.EmailField(primary_key=True)
       password = models.CharField(max_length=20)

       def __str__(self):
              return self.email

class UserDetails(models.Model):
       username = models.CharField(max_length=20, primary_key=True)
       email = models.ForeignKey(Login, to_field="email", on_delete=models.CASCADE)
       userPreferences = models.CharField(max_length=300)
        

       def __str__(self):
              return self.username


from django.db import models

# Create your models here.

class LoginData(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return super().__str__()
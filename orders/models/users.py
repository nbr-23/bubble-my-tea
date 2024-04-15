from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    password_reset_token = models.CharField(max_length=100)
    password_reset_method = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'Users'
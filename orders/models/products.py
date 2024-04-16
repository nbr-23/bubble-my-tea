from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    picture = models.ImageField(upload_to = "images/")
    has_tapioca_perles = models.BooleanField(default=False)
    has_other_perles = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Products'
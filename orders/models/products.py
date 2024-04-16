class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    picture = models.CharField(max_length=250)
    has_tapioca_perles = models.BooleanField(default=False)
    has_other_perles = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Products'
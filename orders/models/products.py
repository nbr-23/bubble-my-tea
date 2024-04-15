class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    picture = models.CharField(max_length=250)
    
    class Meta:
        db_table = 'Products'
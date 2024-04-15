class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Orders'
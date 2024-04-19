from django.db import models
from orders.models.orders import Orders
from orders.models.products import Products 

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sugar_level = models.CharField(max_length=50)
    toppings = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'OrderItem'
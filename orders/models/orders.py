from django.db import models
from orders.models.users import User

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Orders'
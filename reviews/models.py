from django.db import models
from users.models import Customer
from cafes.models import CafeShop


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cafe = models.ForeignKey(CafeShop, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        # Define the table name in the database
        db_table = 'review'

from django.db import models

from users.models import NewUser

class Sales(models.Model):
    user = models.ForeignKey(to=NewUser, on_delete=models.CASCADE)
    date = models.DateField()
    product = models.CharField(max_length=150)
    sales_number = models.PositiveIntegerField()
    revenue = models.FloatField()

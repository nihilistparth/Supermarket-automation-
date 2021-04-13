from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length = 100)
    cost_price = models.FloatField(validators=[MinValueValidator(0.0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    selling_price = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    data = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=0)
    sp = models.JSONField(null=True)
    cp = models.JSONField(null=True)

    def __str__(self):
        return str(self.id)
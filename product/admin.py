from django.contrib import admin
from .models import Product, Transaction
# Register your models here.

admin.site.register(Product)
admin.site.register(Transaction)
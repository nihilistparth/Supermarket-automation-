from django import forms
from .models import Product, Transaction
from django.forms import ValidationError
from django.core.validators import MinValueValidator

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

class EditProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['quantity', 'cost_price' ,'selling_price']

class TransactionForm(forms.ModelForm):
    product_id = forms.IntegerField(required = False)
    Product_name = forms.CharField(max_length=100,required=False)
    quantity = forms.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Transaction
        fields = ['Product_name','quantity','product_id']

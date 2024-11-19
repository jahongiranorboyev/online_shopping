from django import forms
from django.forms import ModelForm

from apps.orders.models import Order, OrderProducts


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields ='__all__'
        exclude = ['user','coupon']

class OrderProductsForm(ModelForm):
    class Meta:
        model = OrderProducts
        fields ='__all__'

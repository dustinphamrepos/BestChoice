from django import forms

from .models import Order, Address


class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'city', 'district', 'precinct', 'address_detail', 'order_note']
    
class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['first_name', 'last_name', 'phone_number', 'email', 'city', 'district', 'precinct', 'address_detail']
    
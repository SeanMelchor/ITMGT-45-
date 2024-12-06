from django.forms import ModelForm
from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    payment_method = forms.ChoiceField(choices=[('card', 'Credit/Debit Card'), ('cash', 'Cash'), ('E-Wallet', 'E-Wallet')])

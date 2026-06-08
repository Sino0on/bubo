from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'phone', 'product', 'color', 'quantity', 'delivery_method', 'comment')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+996 700 000 000', 'type': 'tel'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 99}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Особые пожелания по заказу...'}),
        }

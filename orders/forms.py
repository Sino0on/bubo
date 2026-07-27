from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    # Honeypot: скрытое от людей CSS'ом поле; боты обычно заполняют все поля формы.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'tabindex': '-1',
            'style': 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;',
        }),
    )

    class Meta:
        model = Order
        fields = ('name', 'phone', 'product', 'color', 'quantity', 'delivery_method', 'comment')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+996 700 000 000', 'type': 'tel'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 99}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Особые пожелания по заказу...'}),
        }

    def is_honeypot_filled(self):
        return bool(self.cleaned_data.get('website'))

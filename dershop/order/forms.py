from django import forms

from dershop.order.models import OrderStatus, Order


class OrderStatusForm(forms.ModelForm):
    no = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    status = forms.ChoiceField(choices=OrderStatus.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ["no", "status"]
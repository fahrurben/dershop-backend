from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    parent = forms.ModelChoiceField(queryset=Category.objects.all(), blank=True, required=False, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Category
        fields = ['name', 'parent']

class ProductForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
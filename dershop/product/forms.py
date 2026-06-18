from django import forms
from django.forms.models import inlineformset_factory
from .models import Category, Product, ProductImage


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    parent = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        blank=True,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Category
        fields = ["name", "parent"]


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        blank=True,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Product
        fields = ["name", "category", "description"]


ProductImageFormset = inlineformset_factory(
    Product, ProductImage, fields=["filename"], extra=1, can_delete=True
)

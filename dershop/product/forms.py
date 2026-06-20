from django import forms
from django.forms.models import inlineformset_factory
from .models import Category, Product, ProductImage, Variant


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


class VariantForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.DecimalField(
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": "0.01"}
        ))
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    weight = forms.DecimalField(max_digits=9, decimal_places=2, widget=forms.NumberInput(attrs={"class": "form-control"}))

    class Meta:
        model = Variant
        fields = ["name", "price", "stock", "weight"]


ProductImageFormset = inlineformset_factory(
    Product, ProductImage, fields=["filename"], extra=1, can_delete=True
)

ProductVariantFormset = inlineformset_factory(
    Product, Variant, form=VariantForm, extra=1, can_delete=True,
)

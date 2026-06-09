from django.db import models

from dershop.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='childrens')

    def __str__(self):
        return self.slug

class Product(BaseModel):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    description = models.TextField()

    def __str__(self):
        return self.slug

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    filename = models.CharField(max_length=255)

    def __str__(self):
        return self.filename

class Variant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255)

    # slug format is "productname_variantname"
    slug = models.SlugField(unique=True)

    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.IntegerField()
    weight = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.slug

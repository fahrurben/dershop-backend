from django.db import models

from dershop.common.models import BaseModel
from dershop.product.models import Variant
from dershop.user.models import BaseUser


class OrderStatus(models.TextChoices):
    CREATED = "CR", "Created"
    PAID = "PA", "Paid"
    SHIPPED = "SH", "Shipped"
    DONE = "DO", "Done"


class Order(BaseModel):
    no = models.CharField(max_length=14)
    customer = models.ForeignKey(BaseUser, on_delete=models.RESTRICT)
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=9, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=9, decimal_places=2)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(
        max_length=2, choices=OrderStatus.choices, default=OrderStatus.CREATED
    )

    def __str__(self):
        return self.no


class OrderLine(BaseModel):
    order = models.ForeignKey(
        Order, related_name="order_lines", on_delete=models.RESTRICT
    )
    variant = models.ForeignKey(Variant, on_delete=models.RESTRICT)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    sub_total = models.DecimalField(max_digits=9, decimal_places=2)


class ShippingAddress(BaseModel):
    order = models.OneToOneField(
        Order, related_name="shipping_address", on_delete=models.RESTRICT
    )
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

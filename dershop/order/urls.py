from django.urls import path

from dershop.order.views import (
    OrderListView,

)

urlpatterns = [
    path("order/", OrderListView.as_view(), name="order-list"),
]

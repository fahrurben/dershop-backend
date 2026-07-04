from django.urls import path

from dershop.order.views import (
    OrderListView, order_modal_view,

)

urlpatterns = [
    path("order/", OrderListView.as_view(), name="order-list"),
    path("order/modal-view/<int:id>/", order_modal_view, name="order-view-modal"),
]

from django.urls import path

from dershop.order.views import (
    OrderListView,
    order_modal_view,
    order_modal_edit,
    update_order_view,
)

urlpatterns = [
    path("order/", OrderListView.as_view(), name="order-list"),
    path("order/modal-view/<int:id>/", order_modal_view, name="order-view-modal"),
    path("order/modal-edit/<int:id>/", order_modal_edit, name="order-edit-modal"),
    path("order/modal-update/<int:id>/", update_order_view, name="order-update"),
]

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from dershop.order.forms import OrderStatusForm
from dershop.order.models import Order, OrderStatus


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "order.view_order"
    model = Order
    template_name = "order/list.html"
    context_object_name = "orders"
    paginate_by = 20
    ordering = ["no"]

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your class or instance to the context
        context["status_choices"] = OrderStatus.choices
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            full_name=Concat(
                F("customer__first_name"), Value(" "), F("customer__last_name")
            )
        )
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if query:
            queryset = queryset.filter(
                Q(Q(full_name__icontains=query) | Q(no__icontains=query))
            )

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_template_names(self):
        # Check for the htmx header to return only the list partial
        if self.request.headers.get("HX-Request"):
            return ["order/table.html"]
        return [self.template_name]


@permission_required("order.view_order")
def order_modal_view(request, id):
    order = Order.objects.get(id=id)

    return render(request, "order/modal_view.html", {"order": order})


@permission_required("order.view_order")
def order_modal_edit(request, id):
    order = Order.objects.get(id=id)
    action_url = reverse("order-update", kwargs={"id": id})

    form = OrderStatusForm(instance=order)
    return render(
        request, "order/modal_edit.html", {"form": form, "action_url": action_url}
    )


@permission_required("order.change_order")
@require_http_methods(["POST"])
def update_order_view(request, id):
    """Update product via HTMX."""
    action_url = reverse("category-update", kwargs={"id": id})
    category = get_object_or_404(Order, pk=id)
    form = OrderStatusForm(request.POST, instance=category)
    data = form.data

    if form.is_valid():
        order = Order.objects.get(id=id)
        order.status = data.get("status")
        order.save()

        messages.success(request, "Item updated successfully!")
        response = HttpResponse(status=200)
        response["HX-Redirect"] = reverse("order-list")
        return response
    else:
        return render(
            request, "order/modal_edit.html", {"form": form, "action_url": action_url}
        )

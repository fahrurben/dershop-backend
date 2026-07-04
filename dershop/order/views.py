from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.db.models import Q
from django.urls import reverse

from dershop.order.models import Order, OrderStatus


class OrderListView(LoginRequiredMixin, ListView):
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
        context['status_choices'] = OrderStatus.choices
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            full_name=Concat(F('customer__first_name'), Value(' '), F('customer__last_name'))
        )
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if query:
            queryset = queryset.filter(Q(Q(full_name__icontains=query) | Q(no__icontains=query)))

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_template_names(self):
        # Check for the htmx header to return only the list partial
        if self.request.headers.get("HX-Request"):
            return ["order/table.html"]
        return [self.template_name]

@user_passes_test(lambda u: u.is_staff)
def order_modal_view(request, id):
    order = Order.objects.get(id=id)

    return render(request, "order/modal_view.html", {"order": order})
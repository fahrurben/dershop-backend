from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.generic import ListView

from .forms import ProductForm, CategoryForm
from .models import Category, Product


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category/list.html"
    context_object_name = "categories"

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_template_names(self):
        # Check for the htmx header to return only the list partial
        if self.request.headers.get('HX-Request'):
            return ['category/table.html']
        return [self.template_name]


@user_passes_test(lambda u: u.is_staff)
def category_modal_create(request):
    form = CategoryForm()
    action_url = reverse('category-create')
    return render(request, 'category/modal_create.html', {'form': form, 'action_url': action_url})

@user_passes_test(lambda u: u.is_staff)
def category_modal_edit(request, id):
    category = Category.objects.get(id=id)
    action_url = reverse('category-update', kwargs={'id': id})

    form = CategoryForm(instance=category)
    return render(request, 'category/modal_edit.html', {'form': form, 'action_url': action_url})


@user_passes_test(lambda u: u.is_staff)
@require_POST
def create_category(request):
    """Create a new product via HTMX."""
    form = CategoryForm(request.POST)

    if form.is_valid():
        data = form.data
        category = Category()
        category.name = data.get("name")
        category.slug = slugify(category.name)
        category.parent_id = data.get("parent")
        category.save()

        messages.success(request, "Item created!")
        response = HttpResponse(status=200)
        response['HX-Redirect'] = reverse('category-list')
        return response
    else:
        html = render_to_string('category/category_form.html', {'form': form})
        return HttpResponse(html, status=400)


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def update_category(request, id):
    """Update product via HTMX."""
    action_url = reverse('category-update', kwargs={'id': id})
    category = get_object_or_404(Category, pk=id)
    form = CategoryForm(request.POST, instance=category)
    data = form.data

    if form.is_valid():
        category.name = data.get("name")
        category.slug = slugify(category.name)
        category.parent_id = data.get("parent")
        category.save()

        messages.success(request, "Item updated successfully!")
        response = HttpResponse(status=200)
        response['HX-Redirect'] = reverse('category-list')
        return response
    else:
        # html = render_to_string('category/category_form.html', {'form': form})
        return render(request, 'category/modal_edit.html', {'form': form, 'action_url': action_url})


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["DELETE"])
def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    messages.success(request, "Item deleted successfully!")
    response = HttpResponse(status=200)
    response['HX-Redirect'] = reverse('category-list')
    return response


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/list.html"
    context_object_name = "products"


def product_modal_create(request):
    form = ProductForm()
    return render(request, 'product/modal_create.html', {'form': form})


@login_required
@require_GET
def product_create_view(request):
    form = ProductForm()
    return render(request, 'product/create.html', {'form': form})


@login_required
@require_POST
def create_product(request):
    """Create a new product via HTMX."""
    form = ProductForm(request.POST)

    if form.is_valid():
        data = form.data
        product = Product()
        product.name = data.get("name")
        product.slug = slugify(product.name)
        product.description = data.get("description")
        product.category_id = data.get("category")
        product.save()
        response = HttpResponse(status=200)
        response['HX-Redirect'] = reverse('product-list')
        return response
    else:
        html = render_to_string('product/product_form.html', {'form': form})
        return HttpResponse(html, status=400)

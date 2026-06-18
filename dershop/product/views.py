from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.views.generic import ListView

from .forms import CategoryForm, ProductForm, ProductImageFormset
from .models import Category, Product, ProductImage
from .services import category_create, category_update, product_create, product_update


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category/list.html"
    context_object_name = "categories"
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_template_names(self):
        # Check for the htmx header to return only the list partial
        if self.request.headers.get("HX-Request"):
            return ["category/table.html"]
        return [self.template_name]


@user_passes_test(lambda u: u.is_staff)
def category_modal_create(request):
    form = CategoryForm()
    action_url = reverse("category-create")
    return render(request, "category/modal_create.html", {"form": form, "action_url": action_url})


@user_passes_test(lambda u: u.is_staff)
def category_modal_edit(request, id):
    category = Category.objects.get(id=id)
    action_url = reverse("category-update", kwargs={"id": id})

    form = CategoryForm(instance=category)
    return render(request, "category/modal_edit.html", {"form": form, "action_url": action_url})


@user_passes_test(lambda u: u.is_staff)
@require_POST
def create_category_view(request):
    """Create a new product via HTMX."""
    form = CategoryForm(request.POST)

    if form.is_valid():
        data = form.data
        category = category_create(name=data.get("name"), parent_id=data.get("parent"))

        messages.success(request, "Item created!")
        response = HttpResponse(status=200)
        response["HX-Redirect"] = reverse("category-list")
        return response
    else:
        html = render_to_string("category/category_form.html", {"form": form})
        return HttpResponse(html, status=400)


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def update_category_view(request, id):
    """Update product via HTMX."""
    action_url = reverse("category-update", kwargs={"id": id})
    category = get_object_or_404(Category, pk=id)
    form = CategoryForm(request.POST, instance=category)
    data = form.data

    if form.is_valid():
        category = category_update(category=category, data=data)

        messages.success(request, "Item updated successfully!")
        response = HttpResponse(status=200)
        response["HX-Redirect"] = reverse("category-list")
        return response
    else:
        # html = render_to_string('category/category_form.html', {'form': form})
        return render(request, "category/modal_edit.html", {"form": form, "action_url": action_url})


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["DELETE"])
def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    messages.success(request, "Item deleted successfully!")
    response = HttpResponse(status=200)
    response["HX-Redirect"] = reverse("category-list")
    return response


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/list.html"
    context_object_name = "products"
    paginate_by = 20
    ordering = ["name"]


def product_modal_create(request):
    form = ProductForm()
    return render(request, "product/modal_create.html", {"form": form})


@login_required
@require_GET
def product_create_view(request):
    form = ProductForm()
    return render(request, "product/create.html", {"form": form})


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["GET", "POST"])
def create_product(request):
    """Create a new product via HTMX."""
    product = Product()
    action_url = reverse("product-create")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormset(request.POST, request.FILES)
        if form.is_valid():
            data = form.data
            product = product_create(data=data, image_file=request.FILES.get("images-0-filename"))

            messages.success(request, "Item created successfully!")
            response = HttpResponse(status=200)
            response["HX-Redirect"] = reverse("product-list")
            return response
        else:
            return render(
                request,
                "product/create.html",
                {"form": form, "formset": formset, "action_url": action_url},
            )

    form = ProductForm()
    formset = ProductImageFormset()

    return render(
        request, "product/create.html", {"form": form, "formset": formset, "action_url": action_url}
    )


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["GET", "POST"])
def update_product_view(request, id):
    """Update product via HTMX."""
    product = get_object_or_404(Product, pk=id)
    action_url = reverse("product-update", kwargs={"id": id})

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormset(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            data = form.data
            product = product_update(product=product, data=data)

            instances = formset.save(commit=False)

            for instance in instances:
                # Ensure the foreign key points to our parent recipe
                instance.product = product

                # Manually save to the database
                instance.save()

                # 4. Handle Deletions manually
                # If the user checked the "Delete" checkbox on any row, Django places it here
            for deleted_obj in formset.deleted_objects:
                deleted_obj.delete()

            formset.save_m2m()

            messages.success(request, "Item updated successfully!")
            response = HttpResponse(status=200)
            response["HX-Redirect"] = reverse("product-list")
            return response
        else:
            return render(
                request,
                "product/edit.html",
                {"form": form, "formset": formset, "action_url": action_url},
            )

    form = ProductForm(instance=product)
    formset = ProductImageFormset(instance=product)

    return render(
        request, "product/edit.html", {"form": form, "formset": formset, "action_url": action_url}
    )


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["DELETE"])
def delete_product_view(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    messages.success(request, "Item deleted successfully!")
    response = HttpResponse(status=200)
    response["HX-Redirect"] = reverse("product-list")
    return response

from django.urls import path

from dershop.product.views import CategoryListView, category_modal_create, create_category, category_modal_edit, \
    update_category
from dershop.product.views import ProductListView, create_product, product_create_view, delete_category

urlpatterns = [
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/modal-create/", category_modal_create, name="category-create-modal"),
    path("category/create/", create_category, name="category-create"),
    path("category/modal-edit/<int:id>/", category_modal_edit, name="category-edit-modal"),
    path("category/update/<int:id>/", update_category, name="category-update"),
    path("category/delete/<int:id>/", delete_category, name="category-delete"),

    path("product/", ProductListView.as_view(), name="product-list"),
    path("product/create/", product_create_view, name="product-create-view"),
    path("product/create/", create_product, name="product-create"),
]
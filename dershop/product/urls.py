from django.urls import path

from dershop.product.views import (
    CategoryListView,
    ProductListView,
    category_modal_create,
    category_modal_edit,
    create_category_view,
    create_product,
    delete_category,
    product_create_view,
    update_category_view,
)

urlpatterns = [
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/modal-create/", category_modal_create, name="category-create-modal"),
    path("category/create/", create_category_view, name="category-create"),
    path("category/modal-edit/<int:id>/", category_modal_edit, name="category-edit-modal"),
    path("category/update/<int:id>/", update_category_view, name="category-update"),
    path("category/delete/<int:id>/", delete_category, name="category-delete"),

    path("product/", ProductListView.as_view(), name="product-list"),
    path("product/create/", create_product, name="product-create"),
]
from django.db import transaction
from django.utils.text import slugify

from dershop.common.services import model_update
from dershop.product.models import Category, Product, ProductImage


@transaction.atomic
def category_create(*, name: str, parent_id: int) -> Category:
    slug = slugify(name)
    category = Category.objects.create(name=name, slug=slug, parent_id=parent_id)

    return category


@transaction.atomic
def category_update(*, category: Category, data) -> Category:
    fields: list[str] = ["name", "slug", "parent_id"]

    category, has_updated = model_update(instance=category, fields=fields, data=data)

    category.slug = slugify(data.get("name"))
    category.save()

    return category


@transaction.atomic
def product_create(*, data, image_file) -> Product:
    fields: list[str] = [
        "name",
        "category",
        "description",
        "images-0-filename",
    ]

    slug = slugify(data.get("name"))

    product = Product.objects.create(
        name=data.get("name"),
        slug=slug,
        category_id=data.get("category"),
        description=data.get("description"),
    )

    if image_file is not None:
        product_image = ProductImage.objects.create(product=product, filename=image_file)

    return product


@transaction.atomic
def product_update(*, product: Product, data) -> Product:
    fields: list[str] = [
        "name",
        "category_id",
        "description",
    ]

    product, has_updated = model_update(instance=product, fields=fields, data=data)
    product.slug = slugify(data.get("name"))
    product.save()

    return product

from django.db import transaction
from django.utils.text import slugify

from dershop.common.services import model_update
from dershop.product.models import Category, Product, ProductImage, Variant


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
def product_create(*, request, data) -> Product:
    slug = slugify(data.get("name"))

    product = Product.objects.create(
        name=data.get("name"),
        slug=slug,
        category_id=data.get("category"),
        description=data.get("description"),
    )

    images_total = int(data.get("images-TOTAL_FORMS")[0])

    for i in range(images_total):
        image_file = request.FILES.get(f"images-{i}-filename")
        ProductImage.objects.create(product=product, filename=image_file)

    variant_total = int(data.get("variants-TOTAL_FORMS")[0])

    for i in range(variant_total):
        variant = Variant()
        variant.product = product
        variant.name = data.get(f"variants-{i}-name")
        variant.slug = product.slug + "__" + slugify(data.get(f"variants-{i}-name"))
        variant.price = float(data.get(f"variants-{i}-price"))
        variant.stock = int(data.get(f"variants-{i}-stock"))
        variant.weight = float(data.get(f"variants-{i}-weight"))
        variant.save()

    return product


@transaction.atomic
def product_update(*, request, product: Product, data) -> Product:
    fields: list[str] = [
        "name",
        "category_id",
        "description",
    ]

    product, has_updated = model_update(instance=product, fields=fields, data=data)
    product.slug = slugify(data.get("name"))
    product.save()

    return product

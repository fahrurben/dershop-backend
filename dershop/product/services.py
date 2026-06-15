from django.db import transaction
from django.utils.text import slugify

from dershop.common.services import model_update
from dershop.product.models import Category


@transaction.atomic
def category_create(*, name: str, parent_id: int) -> Category:
    slug = slugify(name)
    category = Category.objects.create(name=name, slug=slug, parent_id=parent_id)

    return category

@transaction.atomic
def category_update(*, category: Category, data) -> Category:
    fields: list[str] = [
        "name",
        "slug",
        "parent_id"
    ]

    category, has_updated = model_update(instance=category, fields=fields, data=data)

    category.slug = slugify(data.get("name"))
    category.save()

    return category

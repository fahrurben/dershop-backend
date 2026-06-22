from django.urls import reverse
from django import template

register = template.Library()

@register.simple_tag
def define_menu_array():
    arr_menu = [
        {"label": "Product", "url": None, "child": [
            {"label": "Category", "url": reverse('category-list'), "child": None },
            {"label": "Product", "url": reverse('product-list'), "child": None },
        ]}
    ]

    return arr_menu

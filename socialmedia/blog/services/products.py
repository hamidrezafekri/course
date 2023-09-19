from django.db.models import QuerySet
from socialmedia.blog.models import Product


def create_products(name: str) -> Product:
    return Product.objects.create(name = name)



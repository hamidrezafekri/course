from django.db import models

# Create your models here.
from socialmedia.common.models import BaseModel


class Product(BaseModel):
    name = models.TextField(max_length=255)
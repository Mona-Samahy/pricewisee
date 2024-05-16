# models.py

from django.db import models
from django.core.exceptions import ValidationError


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description=models.TextField()
    url=models.URLField()
    id = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True,primary_key=True)

    def clean(self):
        if self.price is not None and self.price < 0:
            raise ValidationError("Price must be null or a positive number.")

    def __str__(self):
        return self.name

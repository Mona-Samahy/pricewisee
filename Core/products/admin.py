# admin.py

from django.contrib import admin
from .models import Brand, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price','url','id')

    def brand_name(self, obj):
        return obj.brand.name if obj.brand else None


admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)

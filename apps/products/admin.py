from django.contrib import admin

from apps.products.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

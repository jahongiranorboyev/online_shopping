from django.contrib import admin

from apps.products.models import Product, ProductImage, ProductFeature


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    min_num = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductFeatureInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

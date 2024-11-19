from django.contrib import admin

from apps.orders.models import Order, OrderProducts


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    pass
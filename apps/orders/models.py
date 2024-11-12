from django.utils.timezone import now

from django.conf import settings
from django.db import models

from apps.general.models import PaymentMethod
from apps.products.models import Product


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    payment_method = models.ForeignKey('general.PaymentMethod', on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)

    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)


    coupon = models.ForeignKey('coupons.Coupon', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.pk and self.paid_at is None:
            self.paid_at = now()
        super().save(*args, **kwargs)

class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()


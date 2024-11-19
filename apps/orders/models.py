from django.utils.timezone import now
from django.conf import settings
from django.db import models

from apps.general.models import PaymentMethod
from apps.products.models import Product


class Order(models.Model):
    """
    Model representing a customer's order.

    Attributes:
        created_at (DateTimeField): The timestamp when the order was created.
        user (ForeignKey): The user who placed the order.
        payment_method (ForeignKey): The payment method used for the order.
        total_price (DecimalField): The total price of the order.
        delivery_price (DecimalField): The delivery cost for the order.
        is_paid (BooleanField): Whether the order has been paid for.
        paid_at (DateTimeField): The timestamp when the order was paid.
        coupon (ForeignKey): The coupon used for the order, if any.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    payment_method = models.ForeignKey('general.PaymentMethod', on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    coupon = models.ForeignKey('coupons.Coupon', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        """
        Override the save method to set the paid_at timestamp when the order is paid.

        If the order is updated (i.e., it has a primary key) and `paid_at` is None,
        it will set the `paid_at` field to the current time.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if self.pk and self.paid_at is None:
            self.paid_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the string representation of the Order instance.

        Returns:
            str: The ID of the order.
        """
        return str(self.id)


class OrderProducts(models.Model):
    """
    Model representing a product in an order.

    Attributes:
        order (ForeignKey): The order to which this product belongs.
        product (ForeignKey): The product associated with the order.
        quantity (PositiveIntegerField): The quantity of the product in the order.
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """
        Return the string representation of the OrderProducts instance.

        Returns:
            str: The ID of the order product.
        """
        return str(self.id)

from django.db import models
from django.conf import settings


class Cart(models.Model):
    """
    Represents a user's shopping cart, linking products to users with a quantity.

    Fields:
        user (ForeignKey): The user who owns the cart.
        product (ForeignKey): The product added to the cart.
        quantity (PositiveIntegerField): The quantity of the product in the cart.

    Meta:
        unique_together: Ensures that a user can only add one instance of a product to their cart.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="The user who owns the cart."
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        help_text="The product added to the cart."
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="The quantity of the product in the cart."
    )

    class Meta:
        unique_together = (('user', 'product'),)
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        """
        Returns a string representation of the Cart instance.

        Returns:
            str: A string indicating the user and product in the cart.
        """
        return f"Cart: {self.user} - {self.product} (Quantity: {self.quantity})"


from django.conf import settings
from django.db import models


class Wishlist(models.Model):
    """
    Model representing a user's wishlist for products.

    Attributes:
        user (ForeignKey): The user who owns the wishlist item.
        product (ForeignKey): The product that is added to the wishlist.

    Meta:
        unique_together: Ensures that a user can add a product to their wishlist only once.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'product'),)

    def __str__(self):
        return f"Wishlist: {self.user} - {self.product}"




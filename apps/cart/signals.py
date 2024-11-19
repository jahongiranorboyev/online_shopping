from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.cart.models import Cart


@receiver((post_delete, post_save), sender=Cart)
def cart_post_delete_or_save(instance, **kwargs):
    """
    Signal receiver that updates the user's cart count when a Cart item is saved or deleted.

    This function calculates the total quantity of items in the user's cart and updates the
    `user_cart_count` field of the user.

    Args:
        instance (Cart): The Cart instance that was saved or deleted.
        **kwargs: Additional keyword arguments passed by the signal, typically containing the
                  `sender` and other metadata.
    """
    quantity_sum = Cart.objects.filter(user_id=instance.user_id).aggregate(
        total_quantity=Sum('quantity')
    )['total_quantity'] or 0

    # Update the user's cart count
    instance.user.user_cart_count = quantity_sum
    instance.user.save()

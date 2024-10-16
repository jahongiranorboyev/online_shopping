from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


from apps.cart.models import Cart


@receiver((post_delete,post_save), sender=Cart)
def cart_post_delete_or_save(instance, **kwargs):
    instance.user.user_cart_count = Cart.objects.filter(user_id=instance.user_id).count()
    instance.user.save()
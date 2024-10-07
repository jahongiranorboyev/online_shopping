import os

from django.dispatch import receiver
from django.db.models.signals import post_delete

from apps.products.models import Product


@receiver(post_delete, sender=Product)
def delete_related_image(instance,**kwargs):
    os.remove(instance.image.path)
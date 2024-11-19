import os

from django.dispatch import receiver
from django.db.models.signals import post_delete
from apps.abouts.models import About


@receiver(post_delete, sender=About)
def delete_related_image(instance, **kwargs):
    """
    Deletes the related image file from the filesystem
    when an About instance is deleted.

    Args:
        instance (About): The instance of the About model being deleted.
        **kwargs: Additional keyword arguments provided by the signal.
    """
    image_path = instance.image.path
    if os.path.isfile(image_path):
        os.remove(image_path)

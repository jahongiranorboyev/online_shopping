import os

from django.db.models import ImageField, FileField
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

from apps.products.models import Product


@receiver((post_delete, pre_save))
def delete_related_files(instance, sender, **kwargs):
    for field in sender._meta.get_fields():
        if isinstance(field, (ImageField, FileField)):
            file = getattr(instance, field.name)
            if file and os.path.exists(file.name):
                os.remove(file.path)


def delete_previous_files(instance, sender, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field in sender._meta.get_fields():
        if isinstance(field, (ImageField, FileField)):
            old_file = getattr(old_instance, field.name)
            new_file = getattr(instance, field.name)

            if old_file and old_file != new_file:
                if os.path.exists(old_file.path):
                    os.remove(old_file.path)

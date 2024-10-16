import os

from django.db.models import ImageField, FileField
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save


@receiver((post_delete, pre_save))
def delete_related_files(instance, sender, **kwargs):
    for field in sender._meta.get_fields():
        if isinstance(field, (ImageField, FileField)):
            file = getattr(instance, field.name)
            if file and os.path.exists(file.name):
                os.remove(file.path)

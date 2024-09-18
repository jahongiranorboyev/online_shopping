from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import get_language
from django_ckeditor_5.fields import CKEditor5Field


class About(models.Model):
    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)

    description_uz = CKEditor5Field()
    description_en = CKEditor5Field()
    description_ru = CKEditor5Field()

    image = models.ImageField(upload_to='abouts/images/%Y/%m/%d/')

    def __str__(self):
        return self.title

    @property
    def title(self):
        return getattr(self, f'title_{get_language()}')

    @property
    def description(self):
        return getattr(self, f'description_{get_language()}')

    def clean(self):
        if not self.pk and About.objects.exists():
            raise ValidationError("About object is already created !")



    @classmethod
    def normalize(cls, text):
        """
        This function normalizes the sentence by removing extra spaces
        and returns the normalized sentence.
        """
        return ' '.join(text.split())



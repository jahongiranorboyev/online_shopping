from django.core.exceptions import ValidationError
from django.db import models



class About(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)

    image = models.ImageField(upload_to='abouts/images/%Y/%m/%d/')
    def clean(self):
        if not self.pk and About.objects.exists():
            raise ValidationError("About object is already created !")
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.description = ' '.join(self.description.split())
        self.title = ' '.join(self.title.split())
        super().save(*args, **kwargs)




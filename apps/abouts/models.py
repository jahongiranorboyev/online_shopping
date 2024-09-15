from django.db import models


class About(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)

    image = models.ImageField(upload_to='abouts/images/%Y/%m/%d/')

    def __str__(self):
        return self.title


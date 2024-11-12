from django.db import models


class Service(models.Model):
    """Model to represent a service with a name and an icon."""

    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='services/icons/%Y/%m/%d')

    def __str__(self):
        """Return a string representation of the service name."""
        return self.name



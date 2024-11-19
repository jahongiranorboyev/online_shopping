from django.core.exceptions import ValidationError
from django.db import models


class About(models.Model):
    """
    Represents information about the 'About' section.

    Fields:
        title (str): The title of the about section, limited to 155 characters.
        description (str): A short description, optional, limited to 255 characters.
        image (ImageField): An optional image associated with the about section.
    """

    title = models.CharField(max_length=155, help_text="Title of the about section (max 155 characters).")
    description = models.TextField(
        max_length=255,
        blank=True,
        help_text="Optional short description (max 255 characters)."
    )
    image = models.ImageField(
        upload_to='abouts/images/%Y/%m/%d/',
        help_text="Upload path for the associated image."
    )

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "Abouts"

    def __str__(self):
        """
        Returns the string representation of the About instance.

        Returns:
            str: The title of the about section.
        """
        return self.title

    def clean(self):
        """
        Ensures only one About object can exist in the database.

        Raises:
            ValidationError: If an About object already exists.
        """
        if not self.pk and About.objects.exists():
            raise ValidationError("Only one About object can be created!")


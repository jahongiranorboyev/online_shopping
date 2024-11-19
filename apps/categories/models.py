from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """
    Represents a product category in the system.

    Fields:
        name (CharField): The name of the category.
        image (ImageField): An optional image representing the category.
        parent (ForeignKey): A reference to the parent category for nested categories.

    Meta:
        verbose_name_plural (str): The plural name for the model in the admin interface.
        ordering (list): Specifies the default ordering of categories by name.
    """
    name = models.CharField(
        max_length=255,
        help_text="The name of the category."
    )
    image = models.ImageField(
        upload_to='category/images/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text="An optional image representing the category."
    )
    parent = models.ForeignKey(
        to='self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        related_query_name='category',
        help_text="The parent category for nested categories (optional)."
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def clean(self):
        """
        Custom validation to ensure categories have no more than two levels.

        Raises:
            ValidationError: If a category has more than two levels (parent and grandparent).
        """
        try:
            if not self.pk and self.parent and self.parent.parent:
                raise ValidationError("You can create only two levels of categories.")
        except AttributeError:
            pass

    def __str__(self):
        """
        Returns a string representation of the Category instance.

        Returns:
            str: The name of the category.
        """
        return self.name


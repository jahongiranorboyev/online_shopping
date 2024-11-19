from django.db import models
from django.core.exceptions import ValidationError


class Feature(models.Model):
    """
    Represents a product feature that can be assigned to a category.
    Features are unique and are associated with a category that must be a child category.

    Attributes:
        name (str): The name of the feature.
        category (Category): The category to which the feature belongs, must be a child category.
    """
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        to='categories.Category',
        on_delete=models.PROTECT,
        limit_choices_to={'parent__isnull': False},
    )

    def clean(self):
        """
        Validates that the category assigned to this feature has a parent category.
        Raises a ValidationError if the category does not have a parent.

        Raises:
            ValidationError: If the category does not have a parent.
        """
        if not self.category.parent:
            raise ValidationError({'category': 'Category does not have a parent.'})

    def __str__(self):
        return self.name


class FeatureValue(models.Model):
    """
    Represents a value for a specific feature.
    A feature can have multiple values.

    Attributes:
        feature (Feature): The feature to which this value belongs.
        name (str): The name of the feature value.
    """
    feature = models.ForeignKey(Feature, on_delete=models.PROTECT, related_name='values')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = (('feature', 'name'),)

    def __str__(self):
        return f"{self.name} ({self.feature.name})"

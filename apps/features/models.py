from django.core.exceptions import ValidationError
from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        limit_choices_to={'parent__isnull': False},
        )

    def clean(self):
        if not self.category.parent:
            raise ValidationError({'category': 'not found '})

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']


class FeatureValue(models.Model):
    feature = models.ForeignKey('features.Feature', on_delete=models.PROTECT, related_name='feature_values')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + self.feature.name

    class Meta:
        unique_together = (('feature', 'name'),)
        ordering = ('name',)

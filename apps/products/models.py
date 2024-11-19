from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.categories.models import Category
from apps.comments.models import ProductComment
from apps.general.models import General


class Product(models.Model):
    """
    Represents a product in the store, including details like price, description,
    category, and average ratings.
    """
    title = models.CharField(max_length=155)
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
        default=Decimal(0),
        help_text='Enter in UZS'
    )
    old_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
        help_text='Enter in UZS',
        default=Decimal(0)
    )
    avg_rating = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        default=Decimal('0'),
        editable=False
    )
    comments_count = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=Decimal('0'),
        editable=False
    )
    seen_count = models.PositiveBigIntegerField(default=0, blank=True)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(max_length=10_000, blank=True)
    category = models.ForeignKey(
        'categories.Category', on_delete=models.CASCADE, related_name='products'
    )
    created_at = models.DateField(auto_now_add=True)
    added_at = models.DateField(auto_now=True)
    main_image = models.ImageField(upload_to='products/images/%Y/%m/%d/')

    @property
    def features(self):
        """
        Returns a list of features associated with the product,
        grouped by feature ID, including all values of each feature.
        """
        product_features = ProductFeature.objects.prefetch_related('feature_values').filter(product_id=self.pk)
        features = {}
        for product_feature in product_features:
            for value in product_feature.feature_values.all():
                if value.feature_id not in features:
                    features[value.feature_id] = {
                        'id': value.feature_id,
                        'name': value.feature.name,
                        'values': [{'id': value.id, 'name': value.name}],
                    }
                else:
                    features[value.feature_id]['values'].append({'id': value.id, 'name': value.name})
        return list(features.values())

    def set_avg_rating(self):
        """
        Calculates and updates the average rating for the product based on user comments.
        """
        aggregated_amount = ProductComment.objects.filter(
            product_id=self.pk
        ).aggregate(
            avg=models.Avg('rating', default=0),
        )
        self.avg_rating = round(aggregated_amount['avg'], 1)
        self.save()

    def set_comments_rating(self):
        """
        Updates the comment count for the product.
        """
        self.comments_count = ProductComment.objects.filter(product_id=self.pk).count()
        self.save()

    def __str__(self):
        """
        Returns the title of the product as a string representation.
        """
        return self.title


class ProductImage(models.Model):
    """
    Represents an image associated with a product. Includes an ordering number
    for sorting images.
    """
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/')
    ordering_number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        """
        Returns the string representation of the product image, including the product title.
        """
        return f"Image for {self.product.title}"


class ProductFeature(models.Model):
    """
    Represents a feature associated with a product, which includes feature values
    and related price information.
    """
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='product_features')
    feature_values = models.ManyToManyField('features.FeatureValue', related_name='product_features_values')
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Enter in UZS',
        null=True
    )
    old_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Enter in UZS',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        """
        Override the save method to update product price when a feature is saved.
        """
        super().save(*args, **kwargs)

        # Update the product price based on the feature prices
        self.product.price, self.product.old_price = self.price, self.old_price
        self.product.save()

    def __str__(self):
        """
        Returns a string representation of the product feature with price.
        """
        return f"Feature for {self.product.title} with price {self.price}"

from django.db import models

from apps.categories.models import Category
from apps.comments.models import ProductComment
from apps.ratings.models import ProductRating


class Product(models.Model):
    class Currency(models.TextChoices):
        USD = 'USD', 'United States Dollar'
        EUR = 'EUR', 'Euro'
        JPY = 'JPY', 'Japanese Yen'
        GBP = 'GBP', 'British Pound Sterling'
        AUD = 'AUD', 'Australian Dollar'
        CAD = 'CAD', 'Canadian Dollar'
        CHF = 'CHF', 'Swiss Franc'
        CNY = 'CNY', 'Chinese Yuan'
        SEK = 'SEK', 'Swedish Krona'
        NZD = 'NZD', 'New Zealand Dollar'

    title = models.CharField(max_length=255)
    avg_rating = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        default=0,
        editable=False
    )
    comments_count = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        default=0,
        editable=False
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    old_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency = models.CharField(
        choices=Currency.choices,
        default=Currency.USD,
        max_length=5
    )
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    added_at = models.DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to='products/images/%Y/%m/%d/')

    def set_avg_rating(self):
        aggregated_amount = ProductRating.objects.filter(
            product_id=self.pk
        ).aggregate(
            avg=models.Avg('rating', default=0),
        )
        self.avg_rating = round(aggregated_amount['avg'], 1)
        self.save()

    def set_comments_rating(self):
        self.comments_count = ProductComment.objects.filter(product_id=self.pk).count()
        self.save()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/%Y/%m/%d/')
    ordering_number = models.PositiveSmallIntegerField(default=0)

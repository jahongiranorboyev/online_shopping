from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    """
    A model representing a discount coupon.

    Fields:
        title (CharField): The title of the coupon.
        code (CharField): A unique code representing the coupon.
        start_date (DateField): The date the coupon becomes valid.
        end_date (DateField): The expiration date of the coupon.
        discount_percent (PositiveSmallIntegerField): The percentage discount the coupon provides, between 1 and 100.

    Methods:
        __str__: Returns the string representation of the coupon's title.
    """

    title = models.CharField(max_length=120)
    code = models.CharField(max_length=10, unique=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    discount_percent = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    def __str__(self):
        """
        Returns the string representation of the coupon's title.

        Returns:
            str: The title of the coupon.
        """
        return self.title


class UsedCoupon(models.Model):
    """
    A model representing a coupon that has been used by a user.

    Fields:
        coupon (ForeignKey): The coupon that was used.
        user (ForeignKey): The user who used the coupon.
        created_at (DateTimeField): The timestamp when the coupon was used.

    Methods:
        __str__: Returns a string representation of the coupon usage.
    """

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the used coupon.

        Returns:
            str: A string showing the coupon code and the user who used it.
        """
        return f'{self.coupon.code} used by {self.user}'



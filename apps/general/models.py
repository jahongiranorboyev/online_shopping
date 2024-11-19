from decimal import Decimal
import requests
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.timezone import now
from django.core.cache import cache

from .validation_phone import check_uzb_number


class General(models.Model):
    """
    Represents general settings for the application, such as contact details,
    shipping information, and the default currency.

    Attributes:
        text (str): The text to be displayed, such as business name or slogan.
        address (str): The address of the business (optional).
        email (str): The email address for contact.
        phone (str): A phone number, validated for Uzbekistan format.
        logo (Image): A logo image for the business.
        shipping_percent (int): Shipping percentage to be applied on orders.
    """

    class Currency(models.TextChoices):
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
        RUB = 'RUB', 'RUB'
        UZS = 'UZS', 'UZS'

    DEFAULT_CURRENCY = Currency.UZS

    text = models.CharField(max_length=120)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(help_text="Email address")
    phone = models.CharField(max_length=13, validators=[check_uzb_number], help_text="UZB Number +998123456789")
    logo = models.ImageField(upload_to="general/logo/image/%Y/%m/%d/")
    shipping_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name = "General"
        verbose_name_plural = "General"

    def clean(self):
        """
        Ensures only one General object exists in the database.

        Raises:
            ValidationError: If a General object already exists.
        """
        if not self.pk and General.objects.exists():
            raise ValidationError('Only one General object can exist.')

    def __str__(self):
        return self.text


class GeneralSocialMedia(models.Model):
    """
    Represents a social media link for the business, such as Facebook or Twitter.

    Attributes:
        url (str): The URL of the social media profile.
        icon (Image): The icon image for the social media platform.
    """
    url = models.URLField()
    icon = models.ImageField(upload_to="social_links/icon/image/%Y/%m/%d/")


class CurrencyAmount(models.Model):
    """
    Represents the exchange rate for a specific currency against USD.

    Attributes:
        currency (str): The currency code (e.g., USD, EUR).
        usd_amount (Decimal): The amount of USD that corresponds to 1 unit of the currency.
        date (date): The date of the exchange rate.
    """
    GET_CURRENCY_URL = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/{currency}/all/{date}/'

    currency = models.CharField(max_length=10, choices=General.Currency.choices)
    usd_amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateField()

    @classmethod
    def get_amount(cls, currency: str):
        """
        Fetches the exchange rate for the given currency against USD, using cache
        to reduce redundant API calls.

        Args:
            currency (str): The currency code (e.g., USD, EUR).

        Returns:
            Decimal: The exchange rate for the given currency.
        """
        today = now().date()
        amount_in_uzs = cache.get(f'{currency}_{today}')

        if not amount_in_uzs:
            obj, created = cls.objects.get_or_create(
                currency=currency,
                date=today,
                defaults={
                    'usd_amount': requests.get(cls.GET_CURRENCY_URL.format(
                        currency=currency,
                        date=today)
                    ).json()[0]['Rate'],
                }
            )

            cache.set(f'{currency}_{today}', obj.usd_amount, 24 * 60 * 60)
            amount_in_uzs = cache.get(f'{currency}_{today}')

        return amount_in_uzs

    class Meta:
        unique_together = (('currency', 'date'),)


class PaymentMethod(models.Model):
    """
    Represents a payment method available in the system.

    Attributes:
        name (str): The name of the payment method.
    """
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

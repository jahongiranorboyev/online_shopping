from decimal import Decimal

from django import template

from apps.general.models import CurrencyAmount, General
from apps.wishlist.models import Wishlist

register = template.Library()


@register.simple_tag
def decimal_to_range(decimal_number):
    return range(int(decimal_number))


@register.simple_tag
def product_in_wishlist(user: int, product_id: int) -> bool:
    return Wishlist.objects.filter(user=user, product_id=product_id).exists()


@register.simple_tag
def get_price_by_currency(to_currency: str, price: Decimal = 0) -> Decimal:
    if to_currency == General.Currency.UZS:
        return price
    return round(price / CurrencyAmount.get_amount(currency=to_currency),2)

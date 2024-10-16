from django import template

from apps.wishlist.models import Wishlist

register = template.Library()


@register.simple_tag
def decimal_to_range(decimal_number):
    return range(int(decimal_number))


@register.simple_tag
def product_in_wishlist(user: int, product_id: int) -> bool:
    return Wishlist.objects.filter(user=user, product_id=product_id).exists()

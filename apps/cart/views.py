from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datetime import datetime

from apps.cart.models import Cart
from apps.coupons.models import UsedCoupon
from apps.general.models import General


@login_required(login_url=settings.LOGIN_URL)
def cart(request: WSGIRequest):
    """
    Displays the user's shopping cart, including the total price, shipping, and coupon discounts.

    Args:
        request (WSGIRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered 'cart.html' template with context data for the user's cart.
    """
    try:
        shipping_percent = General.objects.first().shipping_percent
    except AttributeError:
        shipping_percent = 0

    user = request.user
    code = request.session.get('coupon_data', {}).get('code')
    coupon_data = request.session.get('coupon_data')

    if coupon_data:
        end_date = datetime.strptime(coupon_data['end_date'], '%Y-%m-%d').date()
    else:
        end_date = None

    now = datetime.date(datetime.now())

    if (code is not None
            and
            UsedCoupon.objects.filter(coupon__code=code, user_id=user.pk).exists()
            and now == end_date
    ):
        del request.session['coupon_data']

    queryset = Cart.objects.annotate(total_quantity=F('quantity') * F('product__price')).filter(
        user=request.user).select_related('product')

    context = {
        'user_carts': queryset,
        'shipping_percent': shipping_percent,
        'cart_total_price': queryset.aggregate(Sum('total_quantity', default=0))['total_quantity__sum']
    }
    coupon_discount_percent = request.session.get('coupon_data', {}).get('discount_percent', 0)
    total_cart = sum([cart.quantity * cart.product.price for cart in queryset])
    context['total_price'] = total_cart + total_cart * shipping_percent / 100 - total_cart * coupon_discount_percent / 100

    return render(request=request, template_name='cart.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
def create_cart(request: WSGIRequest, product_id: int):
    """
    Adds a product to the user's cart, updating the quantity if it already exists.

    Args:
        request (WSGIRequest): The incoming HTTP request.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponseRedirect: Redirects back to the previous page.
    """
    quantity = request.POST.get('cart_quantity', 1)
    obj, created = Cart.objects.get_or_create(user=request.user, product_id=product_id)
    if obj.quantity != int(quantity):
        obj.quantity = int(quantity)
        obj.save()

    return redirect(request.META['HTTP_REFERER'])


def delete_cart(request: WSGIRequest, product_id: int) -> None:
    """
    Deletes a product from the user's cart.

    Args:
        request (WSGIRequest): The incoming HTTP request.
        product_id (int): The ID of the product to remove from the cart.

    Returns:
        HttpResponseRedirect: Redirects back to the previous page.
    """
    Cart.objects.filter(product_id=product_id).delete()
    return redirect(request.META['HTTP_REFERER'])


def set_cart_quantity(request: WSGIRequest, user_cart_id: int) -> None:
    """
    Updates the quantity of a product in the user's cart or deletes it if quantity is zero or invalid.

    Args:
        request (WSGIRequest): The incoming HTTP request.
        user_cart_id (int): The ID of the cart item to update.

    Returns:
        HttpResponseRedirect: Redirects back to the previous page or 404 page if method is GET.
    """
    if request.method == 'GET':
        return redirect('404-page')

    cart_obj = get_object_or_404(Cart, pk=user_cart_id)

    quantity = request.POST.get('user_cart_quantity', str(cart_obj.quantity))

    if quantity.isdigit() and int(quantity) <= 0:
        cart_obj.delete()
    else:
        cart_obj.quantity = int(quantity)
        cart_obj.save()

    return redirect(request.META['HTTP_REFERER'])

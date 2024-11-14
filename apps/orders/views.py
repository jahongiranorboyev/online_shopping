from pyexpat.errors import messages

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.cart.models import Cart
from apps.general.models import General, PaymentMethod
from apps.orders.forms import OrderForm
from apps.orders.models import Order, OrderProducts


@login_required
def checkout(request):
    carts = Cart.objects.filter(user=request.user).select_related('product')
    if not carts:
        return redirect('carts:cart-page')

    try:
        shipping_percent = General.objects.first().shipping_percent
    except AttributeError:
        shipping_percent = 0
    coupon_discount_percent = request.session.get('coupon_data', {}).get('discount_percent', 0)
    total_cart = sum([cart.quantity * cart.product.price for cart in carts])
    total_sum = total_cart + total_cart * shipping_percent / 100 - total_cart * coupon_discount_percent / 100
    payment_methods = PaymentMethod.objects.order_by('name')

    context = {
        'carts': carts,
        'page': 'pages',
        'shipping_percent': shipping_percent,
        'total_sum': total_sum,
        'total_cart': total_cart,
        'payment_methods': payment_methods,
    }
    return render(request=request, template_name='checkout.html', context=context)

@login_required
@transaction.atomic
def create_order(request):
    print(request.POST)
    carts = Cart.objects.filter(user=request.user).select_related('product')
    order_form = OrderForm(data=request.POST)

    if order_form.is_valid():
        # Save the order object
        order = order_form.save(commit=False)
        order.user = request.POST['user']
        order.total_price = request.POST['total_price']
        order.delivery_price = request.session['delivery_price']
        order.coupon = request.POST['coupon']
        order.save()

        # Loop through items in the cart to create OrderProducts
        for cart_item in carts:
            OrderProducts.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        messages.success(request, 'Your order has been created.')
    else:
        messages.error(request, order_form.errors)

    return redirect('checkouts:checkout')

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from apps.cart.models import Cart


def cart(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect('login-page')
    context = {
        'user_carts': Cart.objects.filter(user=request.user).select_related('product')
    }
    return render(request=request, template_name='cart.html', context=context)


@login_required(login_url='login-page')
def create_cart(request: WSGIRequest, product_id: int):
    if request.method == 'GET':
        redirect('404-page')
    quantity = request.GET.get('cart_quantity', 1)
    obj,created = Cart.objects.get_or_create(product_id=product_id, user=request.user)
    if obj.quantity != quantity:
        obj.quantity = quantity
        obj.save()
    return redirect(request.META['HTTP_REFERER'])


def delete_cart(request: WSGIRequest, product_id: int) -> None:
    if request.method == 'GET':
        redirect('404-page')
    Cart.objects.filter(product_id=product_id).delete()
    return redirect(request.META['HTTP_REFERER'])

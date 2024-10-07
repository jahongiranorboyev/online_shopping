from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from apps.wishlist.models import Wishlist


def wishlist(request: WSGIRequest):
    context = {
        'wishlists': Wishlist.objects.select_related('user', 'product')
    }
    return render(request=request, template_name='wishlist.html', context=context)


def wishlist_create(request: WSGIRequest, product_id: int):
    Wishlist.objects.create(product_id=product_id, user=request.user if request.user.is_authenticated else None)
    return redirect('products:product_list')


def delete_wishlist(request: WSGIRequest, product_id: int) -> None:
    Wishlist.objects.filter(product_id=product_id).delete()
    return redirect('wishlists:wishlist')
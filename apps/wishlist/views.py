from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from apps.wishlist.models import Wishlist


def wishlist(request: WSGIRequest):
    """
    View that renders the user's wishlist.

    If the user is not authenticated, they are redirected to the login page.
    Otherwise, it displays the user's wishlist with related products.
    """
    if not request.user.is_authenticated:
        return redirect('login-page')

    wishlists = Wishlist.objects.filter(user=request.user).select_related('product')

    context = {
        'wishlists': wishlists
    }

    return render(request=request, template_name='wishlist.html', context=context)


@login_required(login_url='login-page')
def wishlist_create(request: WSGIRequest, product_id: int):
    """
    View to add a product to the authenticated user's wishlist.

    If the product is already in the wishlist, it will not be duplicated.
    """
    Wishlist.objects.get_or_create(product_id=product_id, user=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))  # Redirect to the previous page


def delete_wishlist(request: WSGIRequest, product_id: int) -> None:
    """
    View to remove a product from the user's wishlist.

    The product is deleted based on the product_id.
    """
    Wishlist.objects.filter(product_id=product_id, user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))  # Redirect to the previous page


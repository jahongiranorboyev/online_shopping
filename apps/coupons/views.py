from django.contrib import messages
from django.shortcuts import redirect
from apps.coupons.models import Coupon, UsedCoupon


def check_coupon(request):
    """
    Validates a coupon code provided by the user and stores the coupon data in the session if valid.
    If the coupon is invalid, already used, or expired, appropriate messages are shown.

    Args:
        request (HttpRequest): The HTTP request object containing the POST data.

    Returns:
        HttpResponse: Redirects to the previous page with a message based on the coupon validation result.
    """
    code = request.POST.get('coupon_code')

    try:
        # Try to fetch the coupon based on the code
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        # If coupon does not exist, remove any existing coupon data in the session and show an error
        if request.session.get('coupon_data'):
            del request.session['coupon_data']
        messages.error(request, 'The coupon is not valid.')
    else:
        # Check if the user has already used the coupon
        if UsedCoupon.objects.filter(coupon_id=coupon.pk, user_id=request.user.pk).exists():
            # If coupon is already used, remove existing coupon data and show a warning message
            if request.session.get('coupon_data'):
                del request.session['coupon_data']
            messages.warning(request, 'The coupon has already been used.')
        else:
            # If coupon is valid, store coupon data in the session and show success message
            request.session['coupon_data'] = {
                'pk': coupon.pk,
                'code': code,
                'discount_percent': coupon.discount_percent,
                'end_date': coupon.end_date.isoformat(),
            }
            print(request.session.get('coupon_data'))  # Debug print, can be removed in production
            messages.success(request, 'The coupon is valid.')

    return redirect(request.META.get('HTTP_REFERER'))

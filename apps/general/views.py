from django.shortcuts import redirect, render
from django.utils.translation import activate, get_language
from django.conf import settings

from apps.general.models import General
from apps.wishlist.models import Wishlist


def home(request):
    """
    Renders the homepage, displaying all wishlist items.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered homepage template.
    """
    context = {
        'wishlist': Wishlist.objects.all(),
        'page': 'home',
    }
    return render(request, template_name='index.html', context=context)


def cart(request):
    """
    Renders the cart page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered cart page template.
    """
    return render(request=request, template_name='cart.html', context={'page': 'pages'})


def set_language(request, lang):
    """
    Sets the language for the user and redirects back to the previous page.

    Args:
        request (HttpRequest): The request object.
        lang (str): The language code to activate (e.g., 'en', 'fr').

    Returns:
        HttpResponseRedirect: The redirect response to the previous page with the selected language.
    """
    if lang not in settings.MODELTRANSLATION_LANGUAGES:
        lang = settings.LANGUAGE_CODE
    activate(lang)

    host = request.build_absolute_uri('/')
    redirect_to = host + lang + request.META['HTTP_REFERER'].replace(host, '')[2:]

    return redirect(redirect_to)


def set_currency(request, currency: str):
    """
    Sets the currency for the user and redirects to the previous page.

    Args:
        request (HttpRequest): The request object.
        currency (str): The currency code to set (e.g., 'USD', 'EUR').

    Returns:
        HttpResponseRedirect: The redirect response to the previous page.
    """
    currencies = General.Currency.values
    if currency in currencies:
        request.session['currency'] = currency

    return redirect(request.META['HTTP_REFERER'])


def search(request):
    """
    Handles search functionality, storing the search text in the session and redirecting
    to the product list page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: The redirect response to the product list page.
    """
    search_text = request.GET.get('search', '')
    request.session['search_text'] = search_text
    return redirect('products:product_list')


def clear_session(request):
    """
    Clears all session data and redirects to the product list page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: The redirect response to the product list page.
    """
    request.session.flush()
    return redirect('products:product_list')


def page_404(request):
    """
    Renders a custom 404 error page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered 404 error page.
    """
    return render(request, '404.html', status=404)

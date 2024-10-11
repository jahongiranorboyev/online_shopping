from django.shortcuts import redirect, render
from django.utils.translation import activate, get_language

from apps.wishlist.models import Wishlist
from config import settings

def home(request):
    context = {
        'wishlist': Wishlist.objects.all(),
        'page': 'home',
    }
    return render(request, template_name='index.html',context=context)

def checkout(request):
    return render(request=request, template_name='checkout.html', context={'page': 'pages'})


def cart(request):
    return render(request=request, template_name='cart.html', context={'page': 'pages'})


def set_language(request, lang):
    if not lang in settings.MODELTRANSLATION_LANGUAGES:
        lang = settings.LANGUAGE_CODE
    old_lang = get_language()
    activate(lang)
    host= request.build_absolute_uri('/')
    redirect_to=host + lang + request.META['HTTP_REFERER'].replace(host, '')[2:]
    return redirect(redirect_to)

def search(request):
    search_text = request.GET.get('search','')
    request.session['search_text'] = search_text
    return redirect('products:product_list')

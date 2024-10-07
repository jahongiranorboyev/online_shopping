from django.shortcuts import render, redirect

from apps.wishlist.models import Wishlist


def home(request):
    context = {
        'wishlist': Wishlist.objects.all(),
    }
    return render(request, template_name='index.html',context=context)


def detail(request):
    return render(request=request, template_name='detail.html', context={'page': 'detail'})


def contact(request):
    return render(request=request, template_name='contact.html', context={'page': 'contact'})


def checkout(request):
    return render(request=request, template_name='checkout.html', context={'page': 'pages'})


def cart(request):
    return render(request=request, template_name='cart.html', context={'page': 'pages'})

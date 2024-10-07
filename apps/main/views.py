from django.shortcuts import render, redirect


def home(request):
    return render(request, template_name='index.html')


def detail(request):
    return render(request=request, template_name='detail.html', context={'page': 'detail'})


def contact(request):
    return render(request=request, template_name='contact.html', context={'page': 'contact'})


def checkout(request):
    return render(request=request, template_name='checkout.html', context={'page': 'pages'})


def cart(request):
    return render(request=request, template_name='cart.html', context={'page': 'pages'})

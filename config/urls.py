"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from apps.main.views import (
    home, shop, contact, detail,
    checkout, cart, about, login_page,
    user_login, user_register,
    register_page, logout_page
)
from apps.sellers.models import  SellerDetail
from apps.categories.views import category
from django.utils.translation import activate

from config import settings


def test(request):
    language = request.GET.get('language','ru')
    if language is not settings.LANGS:
        language = settings.LANGUAGE_CODE
    activate(language)
    return render(request, 'test.html', {'seller_details': SellerDetail.objects.select_related('seller')})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home-page'),
    path('detail/', detail, name='detail-page'),
    path('contact/', contact, name='contact-page'),
    path('checkout/', checkout, name='checkout-page'),
    path('cart/', cart, name='cart-page'),
    path('shop/', shop, name='shop-page'),
    path('category/', category, name='category-page'),
    path('about/', about, name='about-page'),
    path('login_page/', login_page, name='login-page'),
    path('login/', user_login, name='user_login'),
    path('logout/', logout_page, name='logout-page'),
    path('register_page/', register_page, name='register-page'),
    path('register/', user_register, name='user-register'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('__test/', test, name='test-page'),

]

# if settings.DEBUG:

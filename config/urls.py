
from apps.main import views
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
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
    path('', views.home, name='home-page'),
    path('detail/', views.detail, name='detail-page'),
    path('contact/', views.contact, name='contact-page'),
    path('checkout/', views.checkout, name='checkout-page'),
    path('cart/', views.cart, name='cart-page'),
    path('shop/', views.shop, name='shop-page'),
    path('category/',category, name='category-page'),
    path('wishlist/', views.wishlist, name='wishlist-page'),

    #=======ABOUT URLS =======
    path('about/', include('apps.abouts.urls', namespace='about')),

    #===========AUTH URLS  ============
    path('auth/', include('apps.authentication.urls')),


    path('__debug__/', include('debug_toolbar.urls')),
    path('__test/', test, name='test-page'),

    #=============MEDIA URLS===========
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

]

# if settings.DEBUG:

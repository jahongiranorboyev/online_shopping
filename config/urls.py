from apps.main import views
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from apps.sellers.models import SellerDetail
from apps.categories.views import category
from django.utils.translation import activate

from config import settings

urlpatterns = [
    path('', views.home, name='home-page'),
    path('admin/', admin.site.urls),
    path('detail/', views.detail, name='detail-page'),
    path('contact/', views.contact, name='contact-page'),
    path('checkout/', views.checkout, name='checkout-page'),
    path('cart/', views.cart, name='cart-page'),
    path('products/', include('apps.products.urls',namespace='products')),
    path('category/', category, name='category-page'),
    path('wishlist/', views.wishlist, name='wishlist-page'),

    # =======ABOUT URLS =======
    path('about/', include('apps.abouts.urls', namespace='about')),

    # ===========AUTH URLS  ============
    path('auth/', include('apps.authentication.urls')),

    # =========== CKEDITOR URLS  ============
    path("__ckeditor5/", include('django_ckeditor_5.urls')),

    # =============DEBUG_TOOLBAR URLs =======
    path('__debug__/', include('debug_toolbar.urls')),

    # =============MEDIA URLS===========
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

]

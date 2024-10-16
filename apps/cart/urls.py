from django.urls import path
from apps.cart.views import cart
from apps.cart.views import create_cart, delete_cart

app_name = 'carts'
urlpatterns = [
    path('', cart, name='cart-page'),
    path("create/<int:product_id>/", create_cart, name="create_cart"),
    path("delete/<int:product_id>/", delete_cart, name="delete_cart"),
]

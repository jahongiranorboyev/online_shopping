from django.urls import path

from apps.orders.views import checkout,create_order

app_name = 'checkouts'
urlpatterns = [
    path('', checkout, name='checkout'),
    path('create-order/', create_order, name='create-order'),
]

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class Wishlist(models.Model):
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(to='products.product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.product}"
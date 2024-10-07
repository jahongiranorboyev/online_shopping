from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class Wishlist(models.Model):
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(to='products.product', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'product'),)

    def __str__(self):
        return f"{self.user} - {self.product}"

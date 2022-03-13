from django.db import models
from bakeries.models import ghanadi, mahsool
from accounts.models import Account



class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    mahsool = models.ForeignKey(mahsool, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    kiloo = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.mahsool.price * self.kiloo 

    def __unicode__(self):
        return self.mahsool

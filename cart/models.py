from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class CartAuthCustomer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_customer = models.TextField(verbose_name='Корзина')

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'

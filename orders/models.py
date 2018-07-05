from django.db import models
from index.models import Product
from django.conf import settings
from django.contrib.auth.models import User



class Order(models.Model):
    order_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name='Пользователь',related_name='user_orders')

    first_name = models.CharField(max_length=50,verbose_name='Имя')
    last_name = models.CharField(max_length=50,verbose_name='Фамилия')
    email = models.EmailField()
    address = models.CharField(max_length=250,verbose_name='Адрес доставки')
    postal_code = models.CharField(max_length=20,verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100,verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True,verbose_name='Редактирован')
    paid = models.BooleanField(default=False,verbose_name='Оплаченый')

    class Meta:
        db_table = ('orders_order')
        ordering = ('-created',)
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')

    def __str__(self):
        return 'Заказ № {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    class Meta:
        db_table = ('orders_orderitem')

    order = models.ForeignKey(Order, related_name='items',on_delete=models.SET_NULL,null=True,verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items',on_delete=models.SET_NULL,null=True,verbose_name='Товар')
    price = models.IntegerField(verbose_name='Цена',default=0)
    quantity = models.PositiveIntegerField(default=1,verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

from django.db import models
from django.contrib.auth.models import User
from index.models import Product

class Comment(models.Model):
    class Meta:
        db_table = ('Comments')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    Product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Продукт',related_name='comments')
    User =    models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name='Автор')
    Text =    models.TextField(verbose_name='Комментарий',max_length=1024)
    Created = models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name='Создан')
    Changed = models.DateTimeField(auto_now_add=False,auto_now=True,verbose_name='Изменен')
    Visible = models.BooleanField(default=True,verbose_name='Отображать')
    Like =    models.IntegerField(default=0,verbose_name='Нравится')
    Dislike = models.IntegerField(default=0,verbose_name='Не нравится')

    def get_rating(self):
        rating = int(self.like) - int(self.dislike)
        return rating

    def __str__(self):
        return self.Text[:20]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('index:product_view', args=[str(self.Product.product_slug)])
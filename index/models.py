from django.db import models
from autoslug.fields import AutoSlugField

class Product_brand(models.Model):
    class Meta:
        db_table = ('Product_brand')
        verbose_name = ('Производитель')
        verbose_name_plural = ('Производители')
        ordering = ('brand_name',)

    brand_name = models.CharField(max_length=30,verbose_name='Производитель')
    brand_slug = models.SlugField(max_length=45,verbose_name='Slug')
    brand_country = models.CharField(max_length=50,verbose_name='Страна производства')
    brand_created = models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name='Добавлен')
    brand_changed = models.DateTimeField(auto_now_add=False,auto_now=True,verbose_name='Изменен')

    def __str__(self):
        return "%s" %self.brand_name
    def brand_count(self):
        return Product.objects.filter(product_brand__brand_slug=self.brand_slug).count()

class Product_category(models.Model):
    class Meta:
        db_table = ('Product_category')
        verbose_name = ('Категория продутка')
        verbose_name_plural = ('Категории продуктов')
        ordering = ('category_name',)

    category_name = models.CharField(max_length=20,verbose_name='Категория')
    category_slug = models.SlugField(max_length=20,verbose_name='Slug')
    category_created = models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name='Добавлен')
    category_changed = models.DateTimeField(auto_now_add=False,auto_now=True,verbose_name='Изменен')

    def category_count(self):
        return Product.objects.filter(product_category__category_slug=self.category_slug).count()
    def __str__(self):
        return "%s" %self.category_name

    # def get_absolute_url(self):
    #     from django.urls import reverse
    #     return reverse('index:category_view', args=[str(self.product_slug)])


class Product(models.Model):
    class Meta:
        db_table = ('Product')
        verbose_name = ('Товар')
        verbose_name_plural = ('Товары')
        ordering = ('product_name',)

    product_name = models.CharField(max_length=50,verbose_name='Товар')
    slug = AutoSlugField(populate_from='product_name')
    product_slug = models.SlugField(max_length=65,verbose_name='Slug товара')
    product_brand = models.ForeignKey(Product_brand,on_delete=models.SET_NULL,null=True,verbose_name='Производитель',related_name='brand')
    product_category = models.ForeignKey(Product_category,on_delete=models.SET_NULL,null=True,verbose_name='Категория товара',related_name='category')
    product_description = models.TextField(verbose_name='Описание товара')
    product_new = models.BooleanField(default=False,verbose_name='Новый товар')
    product_price = models.IntegerField(verbose_name='Цена товара',)
    product_old_price = models.IntegerField(default=0,verbose_name='Старая цена')
    product_discount = models.IntegerField(default=0,verbose_name='Скидка в рублях')
    product_visible = models.BooleanField(default=True,verbose_name='Наличие товара/видимость товара')
    product_count =models.IntegerField(default=0,verbose_name='Количество товара на складе')
    product_rating = models.IntegerField(default=50,verbose_name='Рейтинг товара')
    product_like = models.PositiveSmallIntegerField(default=0,verbose_name='Нравится')
    product_dislike = models.PositiveSmallIntegerField(default=0,verbose_name='Не нравится')
    product_views = models.IntegerField(default=0,verbose_name='Просмотры')
    product_created = models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name='Добавлен')
    product_changed = models.DateTimeField(auto_now_add=False,auto_now=True,verbose_name='Изменен')

    def __str__(self):
        return "%s" %self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('index:product_view', args=[str(self.product_slug)])

    def get_rating(self):
        like = int(self.product_like)
        dislike = int(self.product_dislike)
        if like > 0 or dislike > 0:
            value = float(100/(like+dislike))
            value = 100 - value * dislike
        else:
            value = 100
        if value < 9:
            value = 10
        return round(value)

    def get_votes(self):
        return int(self.product_dislike) + int(self.product_like)

#Возвращает текст пути типа (products/apple/iphone 8 plus/image.jpg), для определения пути сохранения изображения товара
def product_picture_directory_path(instance, filename):
    return 'products/{0}/{1}/{2}'.format(instance.product.product_brand.brand_name.replace(' ', '_'), instance.product.product_name.replace(' ', '_'),filename)


class Product_picture(models.Model):
    class Meta:
        db_table = ('Product_picture')
        verbose_name = ('Изображение продукта')
        verbose_name_plural = ('Изображение продуктов')
        ordering = ('picture_created','product')

    product = models.ForeignKey(Product,on_delete=models.SET_NULL,related_name='images',verbose_name='Продукт',null=True)
    picture_image = models.ImageField(upload_to=product_picture_directory_path,verbose_name='Путь')
    picture_created = models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name='Добавлен')
    picture_changed = models.DateTimeField(auto_now_add=False,auto_now=True,verbose_name='Изменен')

    def __str__(self):
        return "%s"%self.product


    def delete(self, *args, **kwargs):
        self.picture_image.delete(save=False)
        super(Product_picture, self).delete(*args, **kwargs)



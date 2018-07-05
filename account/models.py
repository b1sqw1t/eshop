from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime



class Profile(models.Model):
    class Meta:
        db_table = 'Profile_list'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['user']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name='Пользователь',related_name='profile')
    Telephone = models.CharField(max_length=10,verbose_name='Телефон')
    Fax = models.CharField(max_length=10,blank=True,null=True,verbose_name='Факс')
    Company = models.CharField(max_length=50,verbose_name='Организация/компания',blank=True,null=True)
    Adress1 = models.CharField(max_length=100,verbose_name='Адрес1')
    Adress2 = models.CharField(max_length=100,verbose_name='Адрес2',blank=True,null=True)
    City = models.CharField(max_length=30,verbose_name='Город')
    State = models.CharField(max_length=30,verbose_name='Регион/область')
    Country = models.CharField(max_length=30,verbose_name='Страна')
    Zip_code = models.PositiveIntegerField(verbose_name='Почтовый индекс',null=True,blank=True)
    Birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    Other_info = models.TextField(max_length=200,verbose_name='Дополнительная информация',blank=True,null=True)
    image = models.ImageField(upload_to='users/avatar/%Y/%m/%d', verbose_name='Путь до файла',blank=True,null=True)


    def save(self, *args, **kwargs):
        try:
            this_record = Profile.objects.get(id=self.id)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        try:
            if not self.image:
                self.image = 'default/no_photo.jpg'
        except:
            print('ОШИБКА В МЕТОДЕ SAVE!')

        super(Profile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Profile, self).delete(*args, **kwargs)

    def __str__(self):
        return self.user.username




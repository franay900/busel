from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from institutions.models import Institutions


class UserNet(AbstractUser):

    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', null=True, verbose_name='Фотография пользователя',
                               blank=True)
    birth_day=models.DateField(null=True,blank=True,verbose_name='Дата рождения')
    middle_name = models.CharField(max_length=150, verbose_name='Отчество', null=True)
    institution = models.ForeignKey(Institutions, on_delete=models.CASCADE, null=True)
    gender=models.CharField(max_length=150, verbose_name='Пол', null=True)
    class Meta:
        ordering=['last_name','first_name']


    def get_absolute_url(self):
    	return reverse('user_edit',kwargs={'user_id':self.pk})
    def ban(self):
    	return reverse('BanUser',kwargs={'user_id':self.pk})
    def __str__(self):
        return self.last_name+' '+self.first_name+ ' ' + str(self.middle_name)


UserNet._meta.get_field('first_name').blank = False
UserNet._meta.get_field('last_name').blank = False

class FileTemplates(models.Model):
    name=models.CharField(max_length=150,verbose_name='Имя шаблона',null=True)
    file = models.FileField(upload_to='templates/', blank=True)
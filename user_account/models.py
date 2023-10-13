from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from institutions.models import Institutions
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed



class UserNet(AbstractUser):

    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', null=True, verbose_name='Фотография пользователя',
                               blank=True)
    birth_day=models.DateField(null=True,blank=True,verbose_name='Дата рождения')
    middle_name = models.CharField(max_length=150, verbose_name='Отчество', null=True)
    institution = models.ForeignKey(Institutions, on_delete=models.CASCADE, null=True, verbose_name='Организация')
    gender=models.CharField(max_length=150, verbose_name='Пол', null=True)
    registration=models.BooleanField(null=True)
    position=models.CharField(max_length=150, verbose_name='Должность', null=True)
    code = models.CharField(max_length=150, verbose_name = 'Пригласительный код', null=True, blank=True)
    mail_conf = models.BooleanField(default=False)

    class Meta:
        ordering=['last_name','first_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
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



class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    time = models.DateTimeField(verbose_name='Последнее редактирование',auto_now=True,null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_login_failed', ip=ip, username=credentials.get('username', None))
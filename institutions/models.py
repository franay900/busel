from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from user_account.models import *

class Year(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование учебного года')
    start = models.DateField(verbose_name='Дата начала учебного года')
    end = models.DateField(verbose_name='Дата окончания учебного года')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные года'
        ordering = ['-pk']


class TypeInstitutions(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тип организации')
    group = models.ManyToManyField(Group, null=True)

    class Meta:
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы организаций'

    def __str__(self):
        return self.title


class Institutions(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование организации')
    short_title = models.CharField(max_length=50, verbose_name='Краткое наименование')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Фото', blank=True)
    year = models.ForeignKey(Year, on_delete=models.PROTECT, verbose_name='Учебный год')
    typeInstitutions = models.ForeignKey(TypeInstitutions, on_delete=models.PROTECT, verbose_name='Тип', null=True)
    last_edit = models.DateTimeField(verbose_name='Последнее редактирование',auto_now=True,null=True)
    system_mark=models.ForeignKey('SystemMarks',verbose_name='Система оценивания',on_delete=models.PROTECT,default=1)
    is_active=models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Организацию'
        verbose_name_plural = 'Организации'
        ordering = ['-pk']

    def __str__(self):
        return self.title





# Расписание звонков
class BellProfile(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование профиля')
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация')

    def delete_url(self):
        return reverse('Delete_profile_bell', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Расписание звонков'
        verbose_name_plural = 'Профили расписания звонков'
        ordering = ['-pk']



class BellTimetable(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    profile = models.ForeignKey(BellProfile, on_delete=models.CASCADE, verbose_name="Профиль")
    lesson = models.IntegerField(null=True)
    day = models.IntegerField(null=True)


# Уч.Предметы
class Subject(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование предмета')
    short_title = models.CharField(max_length=150, verbose_name='Краткое наименование предмета', null=True)
    institution = models.ForeignKey(Institutions, null=True, blank=True, on_delete=models.CASCADE)

    def delete_url(self):
        return reverse('Delete_subject', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']




# Учебные периоды
class PeriodProfile(models.Model):
    title = models.CharField(max_length=150, verbose_name='Профиль учебного периода')
    year = models.ForeignKey(Year, on_delete=models.PROTECT, verbose_name='Учебный год')
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация')
    typePeriod = models.IntegerField()

    def delete_url(self):
        return reverse('Delete_profile_periods', kwargs={"pk": self.pk})
    def update_url(self):
        return reverse('StudyPeriodsUpdate', kwargs={"profile_pk": self.pk})
    def __str__(self):
        return self.title


class Periods(models.Model):
    profile = models.ForeignKey(PeriodProfile, on_delete=models.CASCADE, verbose_name='Профиль учебного периода')
    start = models.DateField(verbose_name='Дата начала учебного периода')
    end = models.DateField(verbose_name='Дата окончания учебного периода')
    def get_absolute_url(self):
        return reverse('TimetableWeekPk', kwargs={"period": self.pk})

class SystemMarks(models.Model):
    name=models.CharField(max_length=150)
    min_mark=models.IntegerField()
    max_mark=models.IntegerField()

    def __str__(self):
        return self.name
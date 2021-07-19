from django.db import models
from institutions.models import Institutions,Periods
from classes.models import Load,Classes,Student



class LessonType(models.Model):
	name=models.CharField(max_length=150,verbose_name='Наименование типа')
	short_name=models.CharField(max_length=150,verbose_name='Сокращенное наименование типа')
	institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация',null=True,blank=True)
	class Meta:
		verbose_name='Тип урока'
		verbose_name_plural='Типы уроков'
		ordering=['name']
	def __str__(self):
		return self.name
class Lessons(models.Model):
    number = models.IntegerField(null=True)
    date=models.DateField(verbose_name='Дата урока')
    topic=models.CharField(max_length=300, verbose_name='Тема урока',null=True,blank=True)
    homework=models.CharField(max_length=300, verbose_name='Домашнее задание',null=True,blank=True)
    class_pk = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)
    subject_pk = models.ForeignKey(Load, on_delete=models.CASCADE,null=True, verbose_name='Предмет')
    date_homework=models.ForeignKey('Lessons',on_delete=models.SET_NULL,verbose_name='Дата дз',null=True,blank=True)
    types=models.ManyToManyField(LessonType)



class Marks(models.Model):
    student=models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name='Ученик',null=True,blank=True)
    lesson=models.ForeignKey(Lessons, on_delete=models.SET_NULL, verbose_name='Урок',null=True,blank=True)
    lesson_type=models.ForeignKey(LessonType, on_delete=models.SET_NULL, verbose_name='Тип урока',null=True,blank=True)
    mark=models.IntegerField(null=True,blank=True)
    attendance=models.IntegerField(null=True,blank=True)

class MarksItog(models.Model):
    student=models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name='Ученик',null=True,blank=True)
    mark=models.IntegerField(null=True,blank=True)
    load=models.ForeignKey(Load, on_delete=models.SET_NULL, verbose_name='Нагрузка',null=True,blank=True)
    period=models.ForeignKey(Periods, on_delete=models.SET_NULL, verbose_name='Период',null=True,blank=True)
    itog=models.IntegerField(null=True,blank=True)
    not_certified=models.IntegerField(null=True,blank=True)
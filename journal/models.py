from django.db import models
from institutions.models import Institutions,Periods, SystemMarks, Subject, Year
from classes.models import Load,Classes,Student
from user_account.models import UserNet
from django.urls import reverse


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

class TypeExams(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование типа')
    short_name = models.CharField(max_length=10, verbose_name='Сокращенное наименование типа') 
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация',null=True,blank=True)
    class Meta:
        verbose_name='Тип экзамена'
        verbose_name_plural='Типы экзаменов'
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
    teacher=models.ForeignKey(UserNet, on_delete=models.SET_NULL, verbose_name="Учитель",
                                       null=True)
    ktp = models.ForeignKey('TopiCktp', on_delete=models.SET_NULL, null=True)


class Marks(models.Model):
    student=models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name='Ученик',null=True,blank=True)
    lesson=models.ForeignKey(Lessons, on_delete=models.SET_NULL, verbose_name='Урок',null=True,blank=True)
    lesson_type=models.ForeignKey(LessonType, on_delete=models.CASCADE, verbose_name='Тип урока',null=True,blank=True)
    mark=models.IntegerField(null=True,blank=True)
    mark2=models.IntegerField(null=True,blank=True)
    attendance=models.IntegerField(null=True,blank=True)

class MarksItog(models.Model):
    student=models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name='Ученик',null=True,blank=True)
    mark=models.IntegerField(null=True,blank=True)
    
    load=models.ForeignKey(Load, on_delete=models.SET_NULL, verbose_name='Нагрузка',null=True,blank=True)
    period=models.ForeignKey(Periods, on_delete=models.SET_NULL, verbose_name='Период',null=True,blank=True)
    itog=models.IntegerField(null=True,blank=True)
    not_certified=models.IntegerField(null=True,blank=True)

class ReasonSkipping(models.Model):

    reasons=(
            (1,('Уважительная причина')),
            (2,('Неуважительная причина')),
            (3,('По болезни причина'))
        )

    student=models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name='Ученик',null=True,blank=True)
    day=models.DateField()
    reason=models.IntegerField(choices=reasons)


class KTP(models.Model):
    CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5,5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),

    )


    class_number = models.IntegerField(verbose_name='Номер', choices=CHOICES)
    name = models.CharField(max_length=300, verbose_name='Наименование КТП')
    subject_ktp = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.CASCADE)
    author = models.ForeignKey(UserNet, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    institution = models.ForeignKey(Institutions, verbose_name='Организация', on_delete=models.SET_NULL, null=True)
    loads = models.ManyToManyField(Load)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name='Учебный год', null=True)
    def view_ktp(self):
        return reverse('KTP_pk', kwargs={'pk':self.pk})

class Sections_KTP(models.Model):
    ktp = models.ForeignKey(KTP, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, verbose_name='Тема ктп')

class TopiCktp(models.Model):
    name = models.CharField(max_length=700,verbose_name='Наименование')
    section = models.ForeignKey(Sections_KTP, on_delete=models.CASCADE)
    hour = models.IntegerField(verbose_name='Количество часов')
    homework = models.CharField(max_length=700, verbose_name='Домашнее задание')
    
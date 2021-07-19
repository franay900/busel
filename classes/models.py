from django.db import models
from django.urls import reverse
from user_account.models import *
from institutions.models import *


class Classes(models.Model):
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
    letter = models.CharField(max_length=10, verbose_name='Литер')
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация')
    year = models.ForeignKey(Year, on_delete=models.PROTECT, verbose_name='Учебный год')
    сurriculum = models.ForeignKey('Сurriculum', on_delete=models.SET_NULL, verbose_name='Учебный план', null=True)
    bell_profile = models.ForeignKey(BellProfile, on_delete=models.SET_NULL, verbose_name="Профиль звонков", null=True)
    period_profile = models.ForeignKey(PeriodProfile, on_delete=models.SET_NULL, verbose_name="Профиль учебных периодов",
                                       null=True)
    class_teacher=models.ForeignKey(UserNet, on_delete=models.SET_NULL, verbose_name="Классный руководитель",
                                       null=True)
    def get_absolute_url(self):
        return reverse('ClassEdit', kwargs={"pk": self.pk})
    def class_load(self):
        return reverse('LoadPk', kwargs={"pk": self.pk})
    def timetable_templates(self):
        return reverse('TimetableTemplates', kwargs={"pk": self.pk})
    def timetable_weeks(self):
        return reverse('TimetableWeek', kwargs={"pk": self.pk})

    
    class Meta:
        ordering=['class_number','letter']
    def __str__(self):
        return str(self.class_number)+str(self.letter)
class Subgroups(models.Model):
    class_pk = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)
    subject_pk = models.ForeignKey('СurriculumSubject', on_delete=models.CASCADE,null=True, verbose_name='Предмет')
    name = models.CharField(max_length=150, verbose_name='Наименование подгруппы',null=True)
    class Meta:
        ordering=['subject_pk','name']

# Учебный план

class Сurriculum(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование профиля')
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация')
    year = models.ForeignKey(Year, on_delete=models.PROTECT, verbose_name='Учебный год')

    def __str__(self):
        return self.title


class СurriculumSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hour = models.IntegerField(null=True)
    class_number = models.IntegerField()
    profile = models.ForeignKey(Сurriculum, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.title

#нагрузка и расписание 

class Load(models.Model):
    teacher=models.ForeignKey(UserNet, on_delete=models.SET_NULL, verbose_name="Учитель",
                                       null=True)
    class_pk = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)
    subject_pk = models.ForeignKey('СurriculumSubject', on_delete=models.CASCADE,null=True, verbose_name='Предмет')
    subgroup=models.ForeignKey('Subgroups', on_delete=models.CASCADE,null=True, blank=True, verbose_name='Подгруппа')
    class Meta:
        ordering=['subject_pk','subgroup']
    def periods(self):
        return reverse('CheckPeriod', kwargs={"load": self.pk})
class TimetableTemplates(models.Model):
    сurriculum = models.ForeignKey('Сurriculum', on_delete=models.SET_NULL, verbose_name='Учебный план', null=True)
    name = models.CharField(max_length=150, verbose_name='Наименование шаблона',null=True)
    class_pk = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)
    def get_absolute_url(self):
        return reverse('UpdateTimetableTemplate', kwargs={"pk": self.pk})
    class Meta:
        ordering=['name']
class SubjectTemplate(models.Model):
    profile = models.ForeignKey(TimetableTemplates, on_delete=models.CASCADE)
    lesson = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    subject_pk = models.ForeignKey('Load', on_delete=models.CASCADE,null=True, verbose_name='Предмет')


    
#Ученики
class Student(models.Model):
    user=models.ForeignKey(UserNet, on_delete=models.SET_NULL, verbose_name="Пользователь",
                                       null=True)
    class_pk = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.first_name

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
    

    class_number = models.IntegerField(verbose_name='Номер', choices=CHOICES,blank=True)
    letter = models.CharField(max_length=10, verbose_name='Литер', blank=True)
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация')
    year = models.ForeignKey(Year, on_delete=models.PROTECT, verbose_name='Учебный год')
    сurriculum = models.ForeignKey('Сurriculum', on_delete=models.SET_NULL, verbose_name='Учебный план', null=True)
    bell_profile = models.ForeignKey(BellProfile, on_delete=models.SET_NULL, verbose_name="Профиль звонков", null=True)
    period_profile = models.ForeignKey(PeriodProfile, on_delete=models.SET_NULL, verbose_name="Профиль учебных периодов",
                                       null=True)
    class_teacher=models.ForeignKey(UserNet, on_delete=models.SET_NULL, verbose_name="Классный руководитель",
                                       null=True)

    name_group = models.CharField(max_length=10,verbose_name='Наименование группы', blank=True)
    profession_key = models.ForeignKey('Professions',verbose_name='Профессия', blank=True, null=True, on_delete=models.SET_NULL)
    CHANGE_CHOICES = (
    (1, ("Первая смена")),
    (2, ("Вторая смена")),

    )
    change=models.IntegerField(choices=CHANGE_CHOICES, default=1, verbose_name="Смена")   
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
        verbose_name="класс"
        verbose_name_plural="Классы"

    def __str__(self):
        if self.name_group:
            return str(self.name_group)
        else:
            return str(self.class_number)+str(self.letter)
class Subgroups(models.Model):
    class_pk = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)
    subject_pk = models.ForeignKey('СurriculumSubject', on_delete=models.CASCADE,null=True, verbose_name='Предмет')
    name = models.CharField(max_length=150, verbose_name='Наименование подгруппы',null=True)
    class Meta:
        ordering=['subject_pk','name']

# Учебный план

class Сurriculum(models.Model):
    title = models.CharField(max_length=40, verbose_name='Наименование профиля')
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация')
    year = models.ForeignKey(Year, on_delete=models.PROTECT, verbose_name='Учебный год')
    def curriculum_edit(self):
        return reverse('CurriculumEdit', kwargs={"pk": self.pk})
    def curriculum_delete(self):
        return reverse('DeleteCurriculum', kwargs={"pk": self.pk})
    def __str__(self):
        return self.title


class СurriculumSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hour = models.FloatField(null=True)
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


class Professions(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование профессии',null=True)
    training_period = models.CharField(verbose_name='Срок обучения',max_length=30)
    institution = models.ForeignKey(Institutions, on_delete=models.PROTECT, verbose_name='Организация')

    def delete_url(self):
        return reverse('DeleteProfession', kwargs={"pk": self.pk})
    def __str__(self):
        return f'{self.name} ({self.training_period})'

#Ученики
class Student(models.Model):
    user=models.ForeignKey(UserNet, on_delete=models.SET_NULL, verbose_name="Пользователь",
                                       null=True)
    class_pk = models.ForeignKey(Classes, on_delete=models.CASCADE,null=True)
    old_classes = models.ManyToManyField(Classes, null=True, related_name='old_classes')
    date_of_enrollment=models.DateField(verbose_name='Дата зачслениия', default='2021-09-01')
    delete_code = models.CharField(max_length=40, verbose_name='Код удаления', blank=True, null=True)
    def edit(self):
        return reverse('StudentEdit',kwargs={'student_pk':self.pk})
    def __str__(self):
        return  self.user.last_name  + ' ' + self.user.first_name 
    class Meta:
        ordering=['user']
        verbose_name="ученик"
        verbose_name_plural="Ученики"


class StudentSubgroup(models.Model):
    student=models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name="Ученик",
                                       null=True)
    subject=models.ForeignKey(СurriculumSubject, on_delete=models.SET_NULL, verbose_name="Предмет",
                                       null=True)
    subgroup=models.ForeignKey(Subgroups, on_delete=models.SET_NULL, verbose_name="Подгруппа",
                                       null=True)

class StudentShifting(models.Model):

    Shift_CHOICES = (
    (1, ("Зачисление")),
    (2, ("Отчисление")),
    (3, ("Перевод")),

    )
    student=models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name="Ученик",
                                       null=True)


    type_shift = models.IntegerField(null=False, choices=Shift_CHOICES)
    date=models.DateField(verbose_name='Дата')
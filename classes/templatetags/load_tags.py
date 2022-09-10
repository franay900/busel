from django import template
from django.contrib.auth.models import Group
from classes.models import Subgroups, Load,Classes
from institutions.models import BellTimetable


register = template.Library()


@register.simple_tag(name='is_group', takes_context=True)
def is_group(context, subject=0):

    class_ = context['class']
    groups = Subgroups.objects.filter(subject_pk=subject, class_pk=class_)
    if not groups:
        return True


@register.simple_tag(name='get_subgroup', takes_context=True)
def get_subgroup(context, subject=0):
    class_ = context['class']
    return Subgroups.objects.filter(subject_pk=subject, class_pk=class_)


@register.simple_tag(name='get_teacher', takes_context=True)
def get_teacher(context, subject=0, subgroup=None, class_=0):
    class_ = context['class']
    load = Load.objects.filter(subject_pk=subject, subgroup=subgroup, class_pk=class_)
    for load in load:
        if load.teacher:
            teacher = load.teacher.pk
            return teacher
@register.simple_tag(name='get_lesson', takes_context=True)
def get_lesson(context, day=0, num=None):

    class_pk=context['class_pk']
    class_=Classes.objects.get(pk=class_pk)
    bell_lesson=BellTimetable.objects.filter(profile=class_.bell_profile,lesson=num,day=day)
    if bell_lesson:
        for i in bell_lesson:
            bell_lesson_get=BellTimetable.objects.get(pk=i.pk)

        return bell_lesson_get
from django import template
from classes.models import Subgroups, Load,Classes,TimetableTemplates,SubjectTemplate
from journal.models import Lessons
from institutions.models import BellTimetable
from datetime import datetime, timedelta

register = template.Library()


@register.simple_tag(name='get_lesson', takes_context=True)
def get_lesson(context, day=0, num=None):

    class_pk=context['class_pk']
    class_=Classes.objects.get(pk=class_pk)
    bell_lesson=BellTimetable.objects.filter(profile=class_.bell_profile,lesson=num,day=day)
    if bell_lesson:
        for i in bell_lesson:
            bell_lesson_get=BellTimetable.objects.get(pk=i.pk)

        return bell_lesson_get


@register.simple_tag(name='get_subject', takes_context=True)
def get_subject(context, day=0, num=None):
	if 'template' in context:
		template=context['template']
		return SubjectTemplate.objects.filter(profile=template,lesson=num,day=day)

@register.simple_tag(name='check_weeks', takes_context=True)
def check_weeks(context, start=None, end=None):
    class_=context['class']
    check_lessons=Lessons.objects.filter(date__range=[datetime.strptime(str(start), '%d.%m.%Y').strftime('%Y-%m-%d'),datetime.strptime(str(end), '%d.%m.%Y').strftime('%Y-%m-%d')],class_pk=class_)
    if not check_lessons:
        return True
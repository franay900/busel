from django import template
from journal.models import Lessons,Marks,MarksItog
from classes.models import StudentSubgroup
from django.db.models import Q
from institutions.models import Periods


register = template.Library()


@register.simple_tag(name='get_lessons', takes_context=True)
def get_lessons(context,date):
	student = context['student']
	class_student = context['student'].class_pk
	subgroups = StudentSubgroup.objects.filter(student=student)
	arr = []
	for subroup in subgroups:
		arr.append(subroup.subgroup.pk)

	ar = []
	lessons = Lessons.objects.filter(Q(subject_pk__subgroup__pk=None) | Q(subject_pk__subgroup__pk__in=arr),date=date,class_pk=class_student)

	for lesson in lessons:
		homework  = Lessons.objects.filter(date_homework=lesson.pk).first()
		ar.append([lesson,homework])
	return ar



@register.simple_tag(name='get_marks', takes_context=True)
def get_marks(context,lesson):
	student = context['student']
	marks = Marks.objects.filter(lesson=lesson,student=student)
	return marks


@register.simple_tag(name='get_marks_period', takes_context=True)
def get_marks_period(context,period,subject):
	student = context['student']
	
	marks = Marks.objects.filter(lesson__date__gte=period.start,lesson__date__lte=period.end,lesson__subject_pk=subject,student=student)
	arr = []

	for mark in marks:
		if mark.mark:
			arr.append(mark.mark)
		if mark.mark2:
			arr.append(mark.mark2)
	if sum(arr)>0 and len(arr)>0:
		sr_b = round(sum(arr)/len(arr),2)
	else:
		sr_b = '-'
	return marks,sr_b



@register.simple_tag(name='get_marks_itog', takes_context=True)
def get_marks_itog(context,subject,period = None, type_period = None ):
	student = context['student']
	if period is not None and type_period is None:
		marks = MarksItog.objects.filter(load=subject,student=student,period=period).first()
	else:
		marks = MarksItog.objects.filter(load=subject,student=student,itog=type_period).first()
	return marks


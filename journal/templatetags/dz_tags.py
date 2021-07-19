from django import template
from journal.models import Lessons
from institutions.models import BellTimetable
register = template.Library()


@register.simple_tag(name='get_dates', takes_context=True)
def get_dates(context,date):
	load=context['load']
	a=[]
	b=[]
	lesson=Lessons.objects.filter(subject_pk=load,date__gt=date).order_by("date")[:3]
	profile=context['BellProfile']

	return lesson

@register.simple_tag(name='get_bell', takes_context=True)
def get_bell(context,date):

	profile=context['BellProfile']
	weekday=date.date.isoweekday()
	get_day=BellTimetable.objects.filter(lesson=date.number,profile=profile,day=weekday).first()
	return get_day
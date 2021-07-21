from django import template
from journal.models import Marks, MarksItog
register = template.Library()


@register.simple_tag(name='get_marks', takes_context=True)
def get_marks(context,lesosn,type_l,student):
	

	return Marks.objects.filter(student__id=student,lesson=lesosn,lesson_type__id=type_l).first()

@register.simple_tag(name='get_marks_itog', takes_context=True)
def get_marks_itog(context,period,student,load):
	

	return MarksItog.objects.filter(student__id=student,period__id=period,load__pk=load).first()

@register.simple_tag(name='get_itogs', takes_context=True)
def get_itogs(context,itog,student,load):
	

	return MarksItog.objects.filter(student__id=student,itog=itog,load__pk=load).first()
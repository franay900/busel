from django import template
from journal.models import MarksItog

register = template.Library()


@register.simple_tag(name='get_itog', takes_context=True)
def get_itog(context, subject=0, student=0,period=0):

	if period==0:

		return MarksItog.objects.filter(load__subject_pk__pk=subject,student__pk=student, itog=1)
	else:

		return MarksItog.objects.filter(load__subject_pk__pk=subject,student__pk=student, period=period)

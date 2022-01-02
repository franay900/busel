from django import template
from journal.models import Marks, MarksItog
from django.db.models import Sum

register = template.Library()


@register.simple_tag(name='get_marks', takes_context=True)
def get_marks(context,lesosn,type_l,student):
	

	return Marks.objects.filter(student__id=student,lesson=lesosn,lesson_type__id=type_l).first()

@register.simple_tag(name='get_marks_itog', takes_context=True)
def get_marks_itog(context,period,student,load):
	

	return MarksItog.objects.filter(student__id=student,period__id=period,load__pk=load).first()


@register.simple_tag(name='sball_count', takes_context=True)
def sball_count(context,student):
	
	marks=Marks.objects.filter(student=student,lesson__in=context['lessons']).distinct()
	sum_mark=marks.aggregate(Sum('mark'), Sum('mark2'))
	
	if sum_mark['mark__sum']:
		if sum_mark['mark2__sum']:
			count_itog=marks.exclude(mark__isnull=False,attendance=1).count()+marks.exclude(mark2__isnull=False,attendance=1).count()
			sum_itog=sum_mark['mark__sum']+sum_mark['mark2__sum']
		else: 
			print(2)
			count_itog=marks.exclude(mark__isnull=False,attendance=1).count()
			sum_itog=sum_mark['mark__sum']

		ball=sum_itog/count_itog,2

		return sum_itog, count_itog, marks.exclude(mark__isnull=False,attendance=1).count(), marks.exclude(mark__gt=1,attendance=1).count()
		
		

@register.simple_tag(name='get_itogs', takes_context=True)
def get_itogs(context,itog,student,load):
	

	return MarksItog.objects.filter(student__id=student,itog=itog,load__pk=load).first()


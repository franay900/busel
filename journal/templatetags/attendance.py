from django import template
from journal.models import Marks,ReasonSkipping
from datetime import datetime

register = template.Library()


@register.simple_tag(name='get_attendance', takes_context=True)
def get_attendance(context,student,day,year,month):
	
	date=datetime(int(year),int(month),int(day)).strftime('%Y-%m-%d')
	attendance_count=Marks.objects.filter(lesson__date=date, student=student, attendance=1).distinct().count()
	if attendance_count>0:
		return attendance_count
	else:
		return ''


@register.simple_tag(name='get_attendance_reason', takes_context=True)
def get_attendance_reason(context,student,day,year,month):
	
	date=datetime(int(year),int(month),int(day)).strftime('%Y-%m-%d')

	reason=ReasonSkipping.objects.filter(day=date,student=student).first()
	if reason:
		return reason.reason
	else: 
		return ''
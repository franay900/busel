from django import template
from django.contrib.auth.models import Group 
from journal.models import Lessons 
from datetime import datetime

register = template.Library() 

@register.simple_tag(name='get_timetable') 
def get_timetable(user):
    
	lessons=Lessons.objects.filter(teacher=user, date=datetime.today())


	return lessons

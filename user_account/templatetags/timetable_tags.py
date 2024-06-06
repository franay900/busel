from django import template
from django.contrib.auth.models import Group 
from journal.models import Lessons 
from datetime import datetime
from classes.models import Load

register = template.Library() 

@register.simple_tag(name='get_timetable') 
def get_timetable(user):
    
	lessons=Lessons.objects.filter(teacher=user, date=datetime.today())


	return lessons

@register.simple_tag(name='get_journals')
def get_journals(user):
	return Load.objects.filter(teacher=user).order_by('class_pk')
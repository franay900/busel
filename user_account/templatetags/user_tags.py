from django import template
from django.contrib.auth.models import Group 
from classes.models import Classes 


register = template.Library() 

@register.filter(name='is_group') 
def is_group(user):
    groups=user.groups.filter(pk__in=[1])

    return groups.exists()

@register.filter(name='teacher') 
def teacher(user):
	groups=user.groups.filter(name='Учитель')
	if groups:
		return groups.exists()


@register.filter(name='class_manager') 
def class_manager(user):
	
	class_select=Classes.objects.filter(class_teacher=user)
	if class_select:
		return class_select.exists()
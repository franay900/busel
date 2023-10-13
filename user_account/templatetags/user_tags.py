from django import template
from django.contrib.auth.models import Group 
from classes.models import Classes 
from user_account.models import UserNet

register = template.Library() 

@register.filter(name='is_group') 
def is_group(user):
    groups=user.groups.filter(name__in=['Администратор ОО'])

    return groups.exists()

@register.filter(name='teacher') 
def teacher(user):
	groups=user.groups.filter(name='Учитель')
	if groups and not user.groups.filter(name='Администратор ОО'):
		return groups.exists()

@register.filter(name='student') 
def student(user):
	groups=user.groups.filter(name='Ученик')
	if groups:
		return groups.exists()


@register.filter(name='class_manager') 
def class_manager(user):
	
	class_select=Classes.objects.filter(class_teacher=user)
	if class_select:
		return class_select.exists()

@register.simple_tag(name='get_user')
def get_user(username):

	return UserNet.objects.get(username=username)
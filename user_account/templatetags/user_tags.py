from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter(name='is_group') 
def is_group(user):
    groups=user.groups.filter(pk__in=[1])

    return groups.exists()

@register.filter(name='teacher') 
def teacher(user):
	check_admin=user.groups.filter(pk__in=[1])
	groups=user.groups.filter(pk__in=[2])
	if not check_admin:
		return groups.exists()

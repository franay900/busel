from django import template
from django.contrib.auth.models import Group
from classes.models import StudentSubgroup



register = template.Library()


@register.simple_tag(name='subgroup_check', takes_context=True)
def subgroup_check(context, student=0, subject=0):
    
    return StudentSubgroup.objects.filter(student=student,subgroup=subject).first()
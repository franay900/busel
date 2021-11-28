from django import template
from classes.models import Сurriculum,СurriculumSubject, Classes
from django.template.defaultfilters import floatformat



register = template.Library()


@register.simple_tag(name='check_curriculum', takes_context=True)
def check_curriculum(context, curriculum_pk=0):

    return Classes.objects.filter(сurriculum__id=curriculum_pk).first()



@register.simple_tag(name='get_curriculum_subject', takes_context=True)
def get_curriculum_subject(context, subject_pk,class_number):
	try:

		return СurriculumSubject.objects.filter(class_number=class_number,subject__id=subject_pk,profile=context['profile']).first()

	except:
		pass


def formatted_float(value):
    value = floatformat(value, arg=4)
    value=str(value).replace(',','.')
    if value:
    	value='{0:g}'.format(round(float(value),1)) 
    	
    return value


register.filter('formatted_float', formatted_float)
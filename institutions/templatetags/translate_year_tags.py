from django import template
from classes.models import Classes, Student


register = template.Library()


@register.simple_tag(name='get_next_class', takes_context=True)
def get_next_class(context, institution, num,letter):
	
	return Classes.objects.filter(institution=institution,year=institution.year.pk+1, class_number=num+1,letter=letter).first()

@register.simple_tag(name='get_student')
def get_student(pk):

	return Student.objects.filter(class_pk = pk).first()
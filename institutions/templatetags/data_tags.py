from django import template
from user_account.models import UserNet
from institutions.models import Institutions, TypeInstitutions
from classes.models import Classes, Student


register = template.Library()


@register.simple_tag(name='check_data', takes_context=True)
def check_data(context, **kwargs):
	request = context['request']
	institution = Institutions.objects.get(pk=kwargs['institution'])
	type_inst=institution.typeInstitutions.pk
	groups=TypeInstitutions.objects.filter(pk=type_inst).values('group')
	groupsUser=[]
	for i in groups:
		groupsUser.append(i['group'])
	users=UserNet.objects.filter(institution=institution,groups__pk__in=groupsUser,is_active=True).distinct()
	register_users=UserNet.objects.filter(institution=institution,groups__pk__in=groupsUser,is_active=True, registration=True).distinct()
	NumberTeachers = users.count()
	RegisterNumberTeachers = register_users.count()
	classes = Classes.objects.filter(
                institution=request.user.institution.pk,year=request.user.institution.year.pk)
	NumberClasses = classes.count()
	PercentTeacher = round((RegisterNumberTeachers/NumberTeachers) *100,1)
	NumberStudents = Student.objects.filter(class_pk__in=classes,user__is_active=True).count()
	NumberRegister = Student.objects.filter(class_pk__in=classes,user__is_active=True,user__registration=True).count()
	PercentStudent = round(NumberRegister/NumberStudents,1)
	data = [NumberClasses, NumberTeachers, PercentTeacher,NumberStudents, PercentStudent]
	return data
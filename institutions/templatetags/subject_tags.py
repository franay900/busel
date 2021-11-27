from django import template
from classes.models import СurriculumSubject, Сurriculum


register = template.Library()


@register.simple_tag(name='check_subject', takes_context=True)
def check_subject(context, subject_id):
	profiles=Сurriculum.objects.filter(institution=context['institution'])
	return СurriculumSubject.objects.filter(subject__id=subject_id,profile__in=profiles).first()

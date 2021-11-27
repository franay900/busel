from django import template
from institutions.models import BellProfile
from classes.models import Classes


register = template.Library()


@register.simple_tag(name='check_status', takes_context=True)
def check_status(context, bell_profile_pk):
	return Classes.objects.filter(period_profile__id=bell_profile_pk).first()

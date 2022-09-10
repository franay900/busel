from django import template
from journal.models import TopiCktp


register = template.Library()


@register.simple_tag(name='get_topics')
def get_topics(section):
	
	return TopiCktp.objects.filter(section__pk=section).order_by('pk')
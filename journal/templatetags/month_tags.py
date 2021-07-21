from django import template
from modules.weeks import get_dates
from datetime import datetime
register = template.Library()


@register.simple_tag(name='get_months', takes_context=True)
def get_months(context):
	dates=context['lessons']

	sep,octb,nov,dec,jan=0,0,0,0,0
	for date_list in dates:
		if date_list.date.month==9:
			sep+=1
		if date_list.date.month==10:
			octb+=1
		if date_list.date.month==11:
			nov+=1
		if date_list.date.month==12:
			dec+=1
		if date_list.date.month==1:
			jan+=1
	return [sep,octb,nov,dec,jan]
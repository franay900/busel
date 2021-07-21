from django import template
register = template.Library()

@register.filter(is_safe=True)
def myfilter(value):
    return value
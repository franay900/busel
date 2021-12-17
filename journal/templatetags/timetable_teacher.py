from django import template

register = template.Library()


@register.filter
def return_item(l, i):
    try:
        return l[int(i)]
    except:
        return None
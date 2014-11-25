from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='more', is_safe=True)
@stringfilter
def read_more(value):
    KEYWORD = '<!-- Split -->'
    first_index = 0
    last_index = value.find(KEYWORD)

    if(last_index != -1):
        return value[first_index:last_index]
    else:
        return value
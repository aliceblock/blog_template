from django import template

register = template.Library()

@register.filter
def access(var, key):
    return var[key]
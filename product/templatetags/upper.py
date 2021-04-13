from django import template
register = template.Library()

@register.filter
def upper(s):
    return s.upper()
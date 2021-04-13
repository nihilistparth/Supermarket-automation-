from django import template
register = template.Library()

@register.filter
def multiply(a, b):
    return a*b

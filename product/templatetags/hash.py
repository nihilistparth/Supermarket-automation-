from django import template
register = template.Library()

@register.filter
def hash(d, key):
    return d[key-1]

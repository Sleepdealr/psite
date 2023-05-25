from django import template

register = template.Library()


@register.filter
def to_score(value):
    return value.replace(' ', '_')


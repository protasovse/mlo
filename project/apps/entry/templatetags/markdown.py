import mistune
from django import template

register = template.Library()


@register.filter(name='markdown')
def _markdown(value):
    return mistune.markdown(value)

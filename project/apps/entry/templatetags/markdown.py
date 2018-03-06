import misaka
from django import template

register = template.Library()


@register.filter(name='markdown')
def _markdown(value):
    return misaka.html(value)

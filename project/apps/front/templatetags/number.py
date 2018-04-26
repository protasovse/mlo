from django import template
import pymorphy2

register = template.Library()


@register.filter(name='number')
def number(value, arg):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(arg)[0]
    return "{} {}".format(value, word.make_agree_with_number(value).word)
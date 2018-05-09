from django import template
# import pymorphy2

register = template.Library()


@register.filter(name='number')
def number(value, arg):
    # morph = pymorphy2.MorphAnalyzer()
    # word = morph.parse(arg)[0]
    words = arg.split('|')

    vl2 = value - (value // 100 * 100)

    if 4 < vl2 < 21:
        return "{} {}".format(value, words[2])

    vl1 = vl2 - (vl2 // 10 * 10)

    if vl1 == 1:
        return "{} {}".format(value, words[0])
    elif vl1 > 4 or vl1 == 0:
        return "{} {}".format(value, words[2])
    else:
        return "{} {}".format(value, words[1])

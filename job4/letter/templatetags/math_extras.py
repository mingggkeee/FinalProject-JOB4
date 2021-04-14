from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return int(float(value) * int(arg))

@register.filter(name='rating')
def rating_to_int(value):
    if value == '':
        return value
    return int(round(value))
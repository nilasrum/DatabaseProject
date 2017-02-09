from django import template


register = template.Library()


@register.filter('input_type')
def input_type(input):
    return input.field.widget.__class__.__name__

@register.filter('str_cut')
def str_cut(input):
    l = len(input)
    if (l>250):
        s=input[:250]+'...'
        return s
    else:
        return input
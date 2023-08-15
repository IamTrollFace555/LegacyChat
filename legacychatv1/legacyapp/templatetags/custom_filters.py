from django import template

register = template.Library()


@register.filter
def get_attribute(data, attribute_name):
    return data[attribute_name]

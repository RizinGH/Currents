from django import template

register = template.Library()

@register.simple_tag(name='trim_desc')
def trim_desc(s):
    return s.replace("View Full coverage on Google News", '')[:250] + '..'

@register.simple_tag(name='get_list')
def get_list(s):
    s = s.strip('][').replace("'", "").replace(" ", "").split(',')
    return s

@register.simple_tag(name='convert_degree')
def convert_degree(kelvin):
    return round(kelvin -  273.15, 2)
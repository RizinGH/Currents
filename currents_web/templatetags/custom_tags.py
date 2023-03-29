from django import template

register = template.Library()

@register.simple_tag(name='trim_desc')
def trim_desc(s):
    return s.replace("View Full coverage on Google News", '')[:250] + '..'
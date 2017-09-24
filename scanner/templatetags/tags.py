from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if pattern == request.path:
        return 'nav-current'
    return 'nav-link'
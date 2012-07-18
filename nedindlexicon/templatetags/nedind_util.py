# nedind_util tags
from django import template


register = template.Library()

@register.simple_tag
def filter_checkbox(filters, filtername, filterentry):
    if filterentry in filters.get(filtername, []):
        return u' checked="1" '
    return u''
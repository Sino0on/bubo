from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def som(value):
    """Format price: 1200 → '1 200 сом'"""
    try:
        val = int(value)
        formatted = f'{val:,}'.replace(',', ' ')
        return mark_safe(f'{formatted}&nbsp;сом')
    except (TypeError, ValueError):
        return value


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """Return current GET params with overrides, for pagination + filters."""
    request = context['request']
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is None:
            updated.pop(k, None)
        else:
            updated[k] = v
    return updated.urlencode()

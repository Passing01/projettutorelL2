from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplie une valeur par un argument."""
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''

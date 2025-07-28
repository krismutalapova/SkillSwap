from django import template

register = template.Library()


@register.filter
def split(value, delimiter=","):
    """Split a string by delimiter and return a list"""
    if value:
        return [item.strip() for item in value.split(delimiter)]
    return []


@register.filter
def length(value):
    """Return the length of a list or string"""
    try:
        return len(value)
    except:
        return 0


@register.filter
def get_category_name(categories, category_key):
    for key, name in categories:
        if key == category_key:
            return name
    return category_key


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    if dictionary and hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None

from django.template import Library

register = Library()

@register.filter
def resize(value, size):
    """
    Generates the url for the resized image
    return string url
    """
    return "/imagefit/resize/%s%s" % (size, value)

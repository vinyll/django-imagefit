from django.template import Library
try:  # Django >=1.9
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse


register = Library()


@register.filter
def resize(value, size, root_name='resize'):
    """
    Generates the url for the resized image prefixing with prefix_path
    return string url
    """
    return reverse('imagefit_resize', kwargs=dict(
        path_name=root_name, format=size, url=value))


@register.filter
def media_resize(value, size):
    """
    Generates the url for the resized image prefixing with MEDIA_ROOT
    return string url
    """
    return resize(value, size, 'media_resize')


@register.filter
def static_resize(value, size):
    """
    Generates the url for the resized image prefixing with STATIC_ROOT
    return string url
    """
    return resize(value, size, 'static_resize')

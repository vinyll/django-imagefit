from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import get_cache
from django.utils.http import http_date

from imagefit.conf import settings
from imagefit.models import Image, Presets

import os


cache = get_cache(settings.IMAGEFIT_CACHE_BACKEND_NAME)


def _image_response(image):
    response = HttpResponse(
        image.render(),
        image.mimetype
    )
    response['Last-Modified'] = http_date(image.modified)
    return response

def premultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255:
                r = r * a // 255
                g = g * a // 255
                b = b * a // 255
                pixels[x, y] = (r, g, b, a)
    return pixels

def unmultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255 and a != 0:
                r = 255 if r >= a else 255 * r // a
                g = 255 if g >= a else 255 * g // a
                b = 255 if b >= a else 255 * b // a
                pixels[x, y] = (r, g, b, a)
    return pixels

def resize(request, path_name, format, url):
    if path_name == 'static_resize':
        prefix = settings.STATIC_ROOT
    elif path_name == 'media_resize':
        prefix = settings.MEDIA_ROOT
    else:
        prefix = settings.IMAGEFIT_ROOT
    # remove prepending slash
    if url[0] == '/':
        url = url[1:]
    # generate Image instance
    image = Image(path=os.path.join(prefix, url))

    if settings.IMAGEFIT_CACHE_ENABLED:
        image.cache = cache
        image.cached_name = request.META.get('PATH_INFO')
        # shortcut everything, render cached version
        if image.is_cached:
            return _image_response(image)

    # retrieve preset from format argument
    preset = Presets.get(format) or Presets.from_string(format)
    if not preset:
        raise ImproperlyConfigured(
            " \"%s\" is neither a \"WIDTHxHEIGHT\" format nor a key in " +
            "IMAGEFIT_PRESETS." % format
        )

    # Resize and cache image
    image = premultiply(image)
    if preset.get('crop'):
        image.crop(preset.get('width'), preset.get('height'))
    else:
        image.resize(preset.get('width'), preset.get('height'))
    image = unmultiply(image)
    image.save()

    return _image_response(image)

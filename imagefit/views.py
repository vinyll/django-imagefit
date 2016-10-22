from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache
from django.utils.http import http_date

from imagefit.conf import settings
from imagefit.models import Image, Presets

import os


cache = cache.get(settings.IMAGEFIT_CACHE_BACKEND_NAME)


def _image_response(image):
    response = HttpResponse(
        image.render(),
        image.mimetype
    )
    response['Last-Modified'] = http_date(image.modified)
    return response


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
    
    # remove first bread
    url = url[url.find('/'):]
    
    # generate Image instance
    image = Image(path=prefix+url)

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
    if preset.get('crop'):
        image.crop(preset.get('width'), preset.get('height'))
    else:
        print ("PRINTING", preset.get('width'), preset.get('height'))
        image.resize(preset.get('width'), preset.get('height'))
    image.save()

    return _image_response(image)

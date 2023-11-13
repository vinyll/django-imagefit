from django.http import HttpResponse, HttpResponseNotModified
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import caches
from django.utils.http import http_date
from django.views.static import was_modified_since
from inspect import signature


from imagefit.conf import settings
from imagefit.models import Image, Presets

import os
import stat
import time


cache = caches[settings.IMAGEFIT_CACHE_BACKEND_NAME]


def _image_response(image):
    response = HttpResponse(
        image.render(),
        image.mimetype
    )
    response['Last-Modified'] = http_date(image.modified)
    expire_time = getattr(settings, 'IMAGEFIT_EXPIRE_HEADER', 3600 * 24 * 30)
    response['Expires'] = http_date(time.time() + expire_time)
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
    # generate Image instance
    path = os.path.join(prefix, url)
    if not os.path.exists(path):
        return HttpResponse(status=404)
    image = Image(path=path)
    statobj = os.stat(image.path)

    # django.views.static.was_modified_since dropped its size argument in 4.1.
    sig = signature(was_modified_since)

    if not sig.parameters.get('size'):
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                  statobj[stat.ST_MTIME]):
            return HttpResponseNotModified(content_type=image.mimetype)

    if sig.parameters.get('size'):
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                  statobj[stat.ST_MTIME],
                                  statobj[stat.ST_SIZE]):
            return HttpResponseNotModified(content_type=image.mimetype)

    image.cached_name = request.META.get('PATH_INFO')

    if settings.IMAGEFIT_CACHE_ENABLED:
        image.cache = cache
        # shortcut everything, render cached version
        if image.is_cached:
            return _image_response(image)

    # retrieve preset from format argument
    preset = Presets.get(format) or Presets.from_string(format)
    if not preset:
        raise ImproperlyConfigured(
            f" \"{format}\" is neither a \"WIDTHxHEIGHT\" format nor a key in " +
            "IMAGEFIT_PRESETS."
        )

    # Resize and cache image
    if preset.get('crop'):
        image.crop(preset.get('width'), preset.get('height'))
    else:
        image.resize(preset.get('width'), preset.get('height'))
    image.save()

    return _image_response(image)

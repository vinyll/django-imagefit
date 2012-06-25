from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import get_cache

from imagefit.conf import settings
from imagefit.models import Image, Presets

import os


cache = get_cache(settings.IMAGEFIT_CACHE_BACKEND_NAME)


def resize(request, format, url):
    
    # generate Image instance
    image = Image(path=os.path.join(settings.IMAGEFIT_ROOT, url))
    
    if settings.IMAGEFIT_CACHE_ENABLED:
        image.cache = cache
        image.cached_name = request.META.get('PATH_INFO')
        # shortcut everything, render cached version
        if image.is_cached:
            return HttpResponse(
                image.render(),
                image.mimetype
                )

    ## retrieve preset from format argument
    preset = Presets.get(format)
    if not preset:
        preset = Presets.from_string(format)
    else:
        raise ImproperlyConfigured(
            " \"%s\" is neither a \"WIDTHxHEIGHT\" format nor a key in IMAGEFIT_PRESETS." \
            % format
            )
    
    # Resize and cache image
    image.resize(preset.get('width'), preset.get('height'))
    image.save()
    
    return HttpResponse(
            image.render(),
            image.mimetype
            )

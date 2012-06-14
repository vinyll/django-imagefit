from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import get_cache

from PIL import Image

from imagefit.conf import settings

import mimetypes
import StringIO
import os
import re


cache = get_cache(settings.IMAGEFIT_CACHE_BACKEND_NAME)


def resize(request, format, url):
    source = os.path.join(settings.IMAGEFIT_ROOT, url)
    response = HttpResponse(mimetype=mimetypes.guess_type(source)[0])
    cached_name = request.META.get('PATH_INFO')

    # generate image and cache it
    if not cache.has_key(cached_name) or not settings.IMAGEFIT_CACHE_ENABLED:
        image = Image.open(source)
        width_height = tuple()
        
        # force RGB
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        
        ## preset name or width/height
        # get image from conf presets
        presets = getattr(settings, 'IMAGEFIT_PRESETS')
        if format in presets:
            if 'width' and 'height' in presets.get(format):
                preset = presets.get(format)
                width_height = (preset.get('width'), preset.get('height'))
        # get size from url
        elif re.match('(\d+)x(\d+)', format):
            width_height = [int(x) for x in re.match('(\d+)x(\d+)', format).groups()]
        # not a valid size name format
        else:
            raise ImproperlyConfigured(
                " \"%s\" is neither a \"WIDTHxHEIGHT\" format nor a key in IMAGEFIT_PRESETS." \
                % format
                )
        
        # resize
        if width_height:
            image.thumbnail(width_height, Image.ANTIALIAS)
        
        # export to string
        image_str = StringIO.StringIO()
        image.save(image_str, 'png') # not much other supports than png, yet works
        
        # save to cache
        cache.set(request.META.get('PATH_INFO'), image_str.getvalue())
        # generate response
        response.content = image_str.getvalue()
        image_str.close()
    
    # read image from cache
    else:
        response.content = cache.get(cached_name)
    
    return response

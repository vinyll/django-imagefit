from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured

try:
    from PIL import Image
except ImportError:
    raise ImportError("PIL (Python Image Library) package is not installed \
            on your system. Please consider installing it (pip install PIL)")

from imagefit.conf import settings

import os, mimetypes, re


def resize(request, format, url):
    source = os.path.join(settings.IMAGEFIT_ROOT, "media/image.jpg")
    response = HttpResponse(mimetype=mimetypes.guess_type(source)[0])
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
            print width_height
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
    
    # export to response
    image.save(response, 'png') # not much other supports than png, yet works
    return response

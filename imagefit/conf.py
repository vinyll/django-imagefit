from django.conf import settings
from appconf import AppConf

import tempfile
import os


class ImagefitConf(AppConf):

    #: dictionary of preset names that have width and height values
    IMAGEFIT_PRESETS = {
        'thumbnail': {'width': 80, 'height': 80, 'crop': True},
        'medium': {'width': 320, 'height': 240},
        'original': {},
    }

    #: dictionary of output formats depending on the output image extension.
    IMAGEFIT_EXT_TO_FORMAT = {
        '.jpg': 'jpeg', '.jpeg': 'jpeg'
    }

    #: default format for any missing extension in IMAGEFIT_EXT_TO_FORMAT
    #: do not fall-back to a default format but raise an exception if set to None
    IMAGEFIT_EXT_TO_FORMAT_DEFAULT = 'png'

    #: root path from where to read urls
    IMAGEFIT_ROOT = ''

    IMAGEFIT_CACHE_ENABLED = True
    IMAGEFIT_CACHE_BACKEND_NAME = 'imagefit'

    # On Django1.8, this overwrites all CACHES?
    #settings.CACHES[IMAGEFIT_CACHE_BACKEND_NAME] = {
    #    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #    'LOCATION': os.path.join(tempfile.gettempdir(), 'django_imagefit')
    #}

    #: ConditionalGetMiddleware is required for browser caching
    if not 'django.middleware.http.ConditionalGetMiddleware' in settings.MIDDLEWARE_CLASSES:
        settings.MIDDLEWARE_CLASSES += ('django.middleware.http.ConditionalGetMiddleware',)


def ext_to_format(filename):
    extension = os.path.splitext(filename)[1].lower()
    format = settings.IMAGEFIT_EXT_TO_FORMAT.get(extension, settings.IMAGEFIT_EXT_TO_FORMAT_DEFAULT)
    if not format:
        raise KeyError('Unknown image extension: {0}'.format(extension))
    return format

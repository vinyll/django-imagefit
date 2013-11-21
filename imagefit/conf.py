from django.conf import settings
from django.conf import LazySettings

import tempfile
import os


class Settings(LazySettings):

    # Dict of preset names that have width and height values
    IMAGEFIT_PRESETS = getattr(settings, 'IMAGEFIT_PRESETS', {
        'thumbnail': {'width': 80, 'height': 80, 'crop': True},
        'medium': {'width': 320, 'height': 240},
        'original': {},
    })

    # Dict of output formats depending on the output image extension.
    IMAGEFIT_EXT_TO_FORMAT = getattr(settings, 'IMAGEFIT_EXT_TO_FORMAT', {
        '.jpg': 'jpeg', '.jpeg': 'jpeg'
    })

    # Default format for any missing extension in IMAGEFIT_EXT_TO_FORMAT
    # Do not fall-back to a default format but raise an exception if set to None
    IMAGEFIT_EXT_TO_FORMAT_DEFAULT = 'png'

    # Root path from where to read urls
    IMAGEFIT_ROOT = getattr(settings, 'IMAGEFIT_ROOT', '')

    # enable cache backend
    IMAGEFIT_CACHE_ENABLED = getattr(settings, 'IMAGEFIT_CACHE_ENABLED', True)

    # cache backend name
    IMAGEFIT_CACHE_BACKEND_NAME = getattr(settings, 'IMAGEFIT_CACHE_NAME', 'imagefit')

    settings.CACHES = {
        IMAGEFIT_CACHE_BACKEND_NAME: {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(tempfile.gettempdir(), 'django_imagefit')
        }
    }

    # ConditionalGetMiddleware is required for browser caching
    if not 'django.middleware.http.ConditionalGetMiddleware' in settings.MIDDLEWARE_CLASSES:
        settings.MIDDLEWARE_CLASSES += ('django.middleware.http.ConditionalGetMiddleware',)

settings = Settings()


def ext_to_format(filename):
    extension = os.path.splitext(filename)[1].lower()
    format = settings.IMAGEFIT_EXT_TO_FORMAT.get(extension, settings.IMAGEFIT_EXT_TO_FORMAT_DEFAULT)
    if not format:
        raise KeyError('Unknown image extension: {0}'.format(extension))
    return format

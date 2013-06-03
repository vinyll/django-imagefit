from django.conf import settings
from django.conf import LazySettings

import tempfile
import os


class Settings(LazySettings):

    # Dict of preset names that have width and height values
    IMAGEFIT_PRESETS = getattr(settings, 'IMAGEFIT_SIZES', {
        'thumbnail': {'width': 80, 'height': 80, 'crop': True},
        'medium': {'width': 320, 'height': 240},
        'original': {},
        })

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


settings = Settings()

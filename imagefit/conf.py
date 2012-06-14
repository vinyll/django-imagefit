from django.conf import settings
from django.conf import LazySettings

class Settings(LazySettings):
    # Dict of preset names that have width and height values
    IMAGEFIT_PRESETS = getattr(settings, 'IMAGEFIT_SIZES', {
        'thumbnail': {'width': 80, 'height': 80},
        'medium': {'width': 320, 'height': 240},
        'original': {},
        })
    # Root path from where to read urls
    IMAGEFIT_ROOT = ''


settings = Settings()
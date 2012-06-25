from imagefit.conf import settings

from PIL import Image as PilImage

import mimetypes
import StringIO
import re


class Image(object):
    """
    Represents an Image file on the system.
    """
    
    def __init__(self, path, cache=None, cached_name=None, *args, **kwargs):
        self.path = path
        self.pil = PilImage.open(path)
        self.cache = cache
        self.cached_name = cached_name
        
        # force RGB
        if self.pil.mode not in ('L', 'RGB'):
            self.pil = self.pil.convert('RGB')
    
    @property
    def mimetype(self):
        return mimetypes.guess_type(self.path)[0]
    
    @property
    def is_cached(self):
        return self.cache and self.cache.has_key(self.cached_name)
    
    def resize(self, width=None, height=None):
        return self.pil.thumbnail((width, height), PilImage.ANTIALIAS)
    
    def render(self):
        """
        Renders the file content
        """
        if self.is_cached:
            return self.cache.get(self.cached_name)
        else:
            image_str = StringIO.StringIO()
            self.pil.save(image_str, 'png') # not much other supports than png, yet works
            return image_str.getvalue()
    
    def save(self):
        """
        Save the image to the cache if provided and not cached yet.
        """
        if self.cache and not self.is_cached:
            image_str = StringIO.StringIO()
            self.pil.save(image_str, 'png') # not much other supports than png, yet works
            self.cache.set(self.cached_name, image_str.getvalue())
            image_str.close()



class Presets(object):
    """
    Representation of an image format storage
    """
    
    @classmethod
    def get_all(cls):
        """
        Reads presets from settings
        """
        return getattr(settings, 'IMAGEFIT_PRESETS', {})
    
    @classmethod
    def get(cls, key, to_tuple=False):
        """
        Retrieves a specific preset by its name
        """
        preset = cls.get_all().get(key, None)
        if preset:
            if not tuple:
                return preset
            else:
                return (preset.get('width'), preset.get('height'))
    
    @classmethod
    def has(cls, key):
        """
        Checks if a preset exists
        """
        return key in cls.get_all()
    
    @classmethod
    def from_string(cls, string):
        """
        Converts a <width>x<height> into a {'width': <width>, 'height': <height>} dict
        return dict or None
        """
        if re.match('(\d+)x(\d+)', string):
            sizes = [int(x) for x in re.match('(\d+)x(\d+)', string).groups()]
            return {'width': sizes[0], 'height': sizes[1]}
    

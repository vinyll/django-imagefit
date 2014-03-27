from __future__ import division
from imagefit.conf import settings
from PIL import Image as PilImage


import mimetypes
try:
    import StringIO
except ImportError:
    from io import StringIO
import re
import os


class Image(object):
    """
    Represents an Image file on the system.
    """

    def __init__(self, path, cache=None, cached_name=None, *args, **kwargs):
        self.path = path
        self.pil_ = None
        self.cache = cache
        self.cached_name = cached_name



    @property
    def pil(self):
        """
        Load the actual image object only on demand - these can get big.
        """
        
        if self.pil_ is None:
            self.pil_ = PilImage.open(self.path)
            # force RGB
            if self.pil_.mode not in ('L', 'RGBA'):
                self.pil_ = self.pil_.convert('RGBA')
        
        return self.pil_
        
    @pil.setter
    def pil(self, value):
        self.pil_ = value
    
    @property
    def mimetype(self):
        return mimetypes.guess_type(self.path)[0]

    @property
    def modified(self):
        return os.path.getmtime(self.path)

    @property
    def is_cached(self):
        return self.cache and self.cached_name in self.cache

    def resize(self, width=None, height=None):
        return self.pil.thumbnail(
            (int(width), int(height)),
            PilImage.ANTIALIAS)

    def crop(self, width=None, height=None):
        img_w, img_h = self.pil.size
        # don't crop an image than is smaller than requested size
        if img_w < width and img_h < height:
            return self.pil
        elif img_w < width:
            width = img_w
        elif img_h < height:
            height = img_h
        delta_w = img_w / width
        delta_h = img_h / height
        delta = delta_w if delta_w < delta_h else delta_h
        new_w = img_w / delta
        new_h = img_h / delta
        self.resize(new_w, new_h)
        box_diff = ((new_w - width) / 2, (new_h - height) / 2)
        box = (
            int(box_diff[0]), int(box_diff[1]), int(new_w - box_diff[0]),
            int(new_h - box_diff[1]))
        self.pil = self.pil.crop(box)
        return self.pil

    def render(self):
        """
        Renders the file content
        """
        if self.is_cached:
            return self.cache.get(self.cached_name)
        else:
            image_str = StringIO.StringIO()
            ext = self.extension
            self.pil.save(image_str, ext, **settings.IMAGEFIT_FORMAT_SETTINGS.get(ext, {}))
            return image_str.getvalue()

    @property
    def extension(self):
        ext = os.path.splitext(self.cached_name)[1].lower()
        
        try:
            fmt = PilImage.EXTENSION[ext]
        except KeyError:
            PilImage.init()
            try:
                fmt = PilImage.EXTENSION[ext]
            except KeyError:
                fmt = "JPEG"
                #raise KeyError(ext) # unknown extension
        if not fmt:
            fmt = "JPEG"
            
        print(fmt)
        return fmt    
            
    def save(self):
        """
        Save the image to the cache if provided and not cached yet.
        """
        if self.cache and not self.is_cached:
            image_str = StringIO.StringIO()
            # not much other supports than png, yet works
            ext = self.extension
            self.pil.save(image_str, ext, **settings.IMAGEFIT_FORMAT_SETTINGS.get(ext, {}))
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
        return preset

    @classmethod
    def has(cls, key):
        """
        Checks if a preset exists
        """
        return key in cls.get_all()

    @classmethod
    def from_string(cls, string):
        """
        Converts a <width>x<height> into a {'width': <width>,
        'height': <height>} dict
        return dict or None
        """
        if re.match('(\d+)x(\d+),?(\w*)', string):
            sizes = [x for x in re.match(
                '(\d+)x(\d+)(,?[c|C]?)', string).groups()]
            return {
                'width': int(sizes[0]), 'height': int(sizes[1]),
                'crop': bool(sizes[2])}

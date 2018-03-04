# Django Image Fit - Resize an image on the fly

[![Build Status](https://api.travis-ci.org/vinyll/django-imagefit.png)](http://travis-ci.org/vinyll/django-imagefit)

Imagefit allows you to render an image in a template and specify its dimensions.
It preserves the original image file.

It is compatible with various sources of images such as django-filebrowser's
FileBrowseField, user uploaded images, static images, …

Works on Python 3.x and Python 2.6 or more; Django 1.4 > 2.0.


#### Benefits

* only 1 image file exists on the server, therefore it's always easy to replace
and adapt the image per template or zone.
* no model to adapt for large image and thumbnail that may vary when redesigning
the website.
* perfect match with mediaqueries to adapt on mobile, tablets and
multi-size screens.
* better quality than html/css resizing and no large file download, great for
lower bandwidth.


#### Quick tour

Example 1: render _/static/myimage.png_ image at a maximum size of 200 x 150 px:

```html
{{ "/static/myimage.png"|resize:"200x150" }}
```

Example 2: render model's _news.image_ as a thumbnail:

```html
{{ news.image|resize:"thumbnail" }}
```

Example 1: render _/static/myimage.png_ image at a maximum cropped size of 150 x 150 px:

```html
{{ "/static/myimage.png"|resize:"150x150,C" }}
```

#### What this is not

* For creating specific model fields that resize image when model saves, see
[django-imagekit](https://github.com/matthewwithanm/django-imagekit)
* If you wish to avoid very large image on the server, consider resizing your original image
before uploading it


## Installation

#### Download

Via pip ![latest version](https://img.shields.io/pypi/v/django-imagefit.svg)

```bash
pip install django-imagefit
```

or the bleeding edge version

```
pip install -e git+https://github.com/vinyll/django-imagefit.git#egg=django-imagefit
```

#### update INSTALLED_APPS

In _settings.py_, add _imagefit_ in your INSTALLED_APPS

```python
INSTALLED_APPS = (
    …,
    'imagefit',
)
```

And add the path relative to your project (see _configuration_ below)

```python
IMAGEFIT_ROOT = "public"
```

#### urls.py

Imagefit is a resize service, therefore include its urls.

Prefix it with whatever you want (here "imagefit" for example):

```python
urlpatterns = urlpatterns('',
    …
    url(r'^imagefit/', include('imagefit.urls')),
)
```

Congratulations, you're all set!


## Usage

your_template.html

```html
{% load imagefit %}

<img src="{{ "/static/image.png"|resize:'thumbnail' }}" />
<img src="{{ "/static/image.png"|resize:'320x240' }}" />
<img src="{{ "/static/image.png"|resize:'320x240,C' }}" />
```

This will display your _/static/image.png_:

1. in the _thumbnail_ format (80 x 80 px)
2. resized in a custom 320 x 240 pixels
3. resized and cropped in a custom 320 x 240 pixels

> the _,C_ modifier stands for _Cropping_

## Configuration

#### Root path

You should most probably customize the path to the root folder of your images.
The url your specify in your model will be concatenated to this IMAGEFIT_ROOT
to find the appropriate image on your system.

The path will be relative to the project folder.

If starting with a "/", it will be an absolute path (quid about Windows).

```python
IMAGEFIT_ROOT = "public"
```

So with this example the image url "/static/image.png" would be pointing to
_/PATH/TO/YOUR/PROJECT/**public/static/image.png**_

#### Templatetags

    resize(value, size)  # path is relative to you settings.IMAGE_ROOT
    static_resize(value, size)  # path is relative to you settings.STATIC_ROOT
    media_resize(value, size)  # path is relative to you settings.MEDIA_ROOT

Can be used in templates as so :

    {{ "/static/logo.png"|resize:'320x240' }}
    {{ "logo.png"|static_resize:'320x240' }}
    {{ "user_avatar.png"|media_resize:'320x240' }}


#### Presets

Presets are configuration names that hold width and height (and maybe more later on).
Imagefit is already shipped with 3 presets : _thumbnail_ (80x80), _medium_ (320x240)
and _original_ (no resizing).

You may override them or create new ones through settings.py


Custom presets examples :

```python
IMAGEFIT_PRESETS = {
    'thumbnail': {'width': 64, 'height': 64, 'crop': True},
    'my_preset1': {'width': 300, 'height': 220},
    'my_preset2': {'width': 100},
}
```


#### Cache

Because resizing an image on the fly is a big process, django cache is enabled
by default.

Therefore you are strongly invited to set your imagefit cache preferences to
False for local development.

You can customize the default cache preferences by overriding default values
described below via settings.py :

```python
# enable/disable server cache
IMAGEFIT_CACHE_ENABLED = True
# set the cache name specific to imagefit with the cache dict
IMAGEFIT_CACHE_BACKEND_NAME = 'imagefit'
CACHES = {
    'imagefit': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(tempfile.gettempdir(), 'django_imagefit')
        }
    }
```

Note that `CACHES` default values will be merge with yours from _settings.py_


#### Formats

Imagefit uses PIL to resize and crop the images and this library requires to
specify the format of the output file. Imagefit allows you to specify an output
format depending of the output filename. Please note that the the output extension
is left unchanged.

You can customize the default mapping by overriding default values described below
via settings.py :

```python
# Example extension -> format.
IMAGEFIT_EXT_TO_FORMAT = {'.jpg': 'jpeg', '.bmp': 'png'}
# Disallow the fall-back to a default format: Raise an exception in such case.
IMAGEFIT_EXT_TO_FORMAT_DEFAULT = None
```


#### Expires Header

Django Imagefit comes with Expires header to tell the browser whether it should request the resource from the server or use the cached version.  
This has two core benefits. The browser will be using the cached version of the resource in the second load and page load will be much faster. Also, it will require fewer requests to the server. 

As a page score parameter, static resources used in a web page should be containing an Expires information for better performance.

The default value of the expires header is set to 30 days from now. You can override this value via settings.py as:

```python
IMAGEFIT_EXPIRE_HEADER = 3600  # for 1 hour
```

## Troubleshooting


### "decoder jpeg not available" on Mac OSX


You may have installed PIL through pip or easy_install that
does not install libjpeg dependency.

If so :

1. Uninstall pil via pip
2. Install pip via homebrew: `brew install pil`
3. Reinstall pil via pip: `pip install pil`


## Todo

* Refactor _views.resize_
* Make resize quality/speed configurable
* More examples for doc
* enable URL images in addition to system files

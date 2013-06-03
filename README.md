# Django Image Fit - Resize image on demand

Imagefit allows you to render an image in a template where you specify its width and height
while preserving the original image.

It is as easy to use as html resizing but without the .

It is fully compatible with various sources of images :
django-filebrowser FileBrowseField, uploaded imagem, static image, and others.


#### Benefits

* only 1 image file exist, therefore it remains easy to replace and adapt per template and zone
* no model to adapt for large image and thumbnail that may vary with template refactoring
* perfect match with mediaqueries to adapt on mobile, tablets and multi-size screens
* better quality than html/css resizing and no big file downloaded, great for lower bandwidth


#### Quick tour

Example 1: render "/static/myimage.png" image at a maximum size of 200 x 150 px :

    {{ "/static/myimage.png"|resize:"200x150" }}

Example 2: render model's "news.image" as a thumbnail :

    {{ news.image|resize:"thumbnail" }}

Example 1: render "/static/myimage.png" image at a maximum cropped size of 150 x 150 px :

    {{ "/static/myimage.png"|resize:"150x150,C" }}


#### What this is not

* For creating specific model fields that resize image when model saves, see django-imagekit
* If you wish to avoid very large image on the server, consider resizing your original image
before uploading it



## Installation

#### Download

#### update INSTALLED_APPS

In settings.py, add "imagefit" in your INSTALLED_APPS

    INSTALLED_APPS = (
    	…,
    	'imagefit',
    )

And add the path relative to your project (see _configuration_ below)

    IMAGEFIT_ROOT = "public"

#### urls.py

Imagefit is a resize service, therefore include its urls.

Prefix it with whatever you want (here "imagefit" for example) :

    urlpatterns = urlpatterns('',
        …
        url(r'^imagefit/', include('imagefit.urls')),
    )

Congratulations, you're all set !


## Usage

your_template.html

    {% load imagefit %}

    <img src="{{ "/static/image.png"|resize:'thumbnail' }}" />
    <img src="{{ "/static/image.png"|resize:'320x240' }}" />
    <img src="{{ "/static/image.png"|resize:'320x240,C' }}" />

This will display your /static/image.png :

1. in the thumbnail format (80 x 80 px)
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

	IMAGEFIT_ROOT = "public"

So with this example the image url "/static/image.png" would be pointing to
/PATH/TO/YOUR/PROJECT/**public/static/image.png**

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
Imagefit is already shipped with 3 presets : "thumbnail" (80x80),"medium" (320x240)
and "original" (no resizing).

You may override them through settings.py


Custom presets examples :

    IMAGEFIT_PRESETS = {
        'thumbnail': {'width': 64, 'height': 64, 'crop': True},
        'my_preset1': {'width': 300, 'height': 220},
        'my_preset2': {'width': 100},
    }


#### Cache

Because resizing an image on the fly is a big process, django cache is enabled 
by default.

Therefore you are strongly invited to set your imagefit cache preferences to 
False for local development.

You can customize the default cache preferences by overriding default values 
described below via settings.py :

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

Note that CACHES default values will be merge with yours from settings.py


## troubleshooting


### "decoder jpeg not available" on Mac OSX


You may have installed PIL through pip or easy_install that
does not install libjpeg dependency.

If so :

1. Uninstall pil via pip
2. Install pip via homebrew : brew install pil
3. Reinstall pil via pip : pip install pil


## Todo

* Refactor views.resize
* Make resize quality/speed configurable
* More examples for doc
* enable URL images in addition to system files

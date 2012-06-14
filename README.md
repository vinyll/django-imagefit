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



#### What this is not

* For cropping or altering image, use PIL or Pillow
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


#### urls.py

Imagefit is a resize service, therefore include its urls.

Prefix it with whatever you want (here "imagefit" for example) :

    urlpatterns = urlpatterns('',
        …
        url(r'^imagefit/', include('imagefit.urls')),
    )


## Configuration


#### Root path

You MUST specify the path to the root folder of your images.
The url your specify in your model will be concatenated to this IMAGEFIT_ROOT
to find the appropriate image on your system.

	IMAGEFIT_ROOT = "/root/to/image/base/dir"


Congratulations, you're done !


## Usage

your_template.html

	{% load imagefit %}
	
	<img src="{{ "/static/image.png"|resize:'thumbnail' }}" />
	<img src="{{ "/static/image.png"|resize:'320x240' }}" />

This will display your /static/image.png in the thumbnail format (80 x 80 px)
and below in a custom 320 x 240 pixels.

## Advanced configuration

#### Presets

Presets are configuration names that hold width and height (and maybe more later on).
Imagefit is already shipped with 3 presets : "thumbnail" (80x80), 
"medium" (320x240) and "original" (no resizing).

You may override them through settings.py


Custom presets examples :

    IMAGEFIT_PRESETS = {
        'thumbnail': {'width': 64, 'height': 64},
        'my_preset1': {'width': 300, 'height': 220},
        'my_preset2': {'width': 100},
    }


## troubleshooting


### "decoder jpeg not available" on Mac OSX


You may have installed PIL through pip or easy_install that
does not install libjpeg dependency.

If so :

1. Uninstall pil via pip
2. Install pip via homebrew : brew install pil
3. Reinstall pil via pip : pip install pil


## Todo

* Use cache
* Make resize quality/speed configurable

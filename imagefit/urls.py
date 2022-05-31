from . import views

# EAFP compliance with version 4.0
try:
    from django.conf.urls import url
except ImportError as e:
    from django.urls import re_path
    from django.utils import version

    # in case of any other error
    if int(version.get_version().split('.')[0]) >= 4:
        url = re_path
    else:
        raise ImportError(str(e))

urlpatterns = [
    url(
        r'^(?P<path_name>[\w_-]*)/(?P<format>[,\w-]+)/(?P<url>.*)/?$',
        views.resize,
        name="imagefit_resize"),
]

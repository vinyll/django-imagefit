from django.urls import re_path
from . import views


urlpatterns = [
    re_path(
        r'^(?P<path_name>[\w_-]*)/(?P<format>[,\w-]+)/(?P<url>.*)/?$',
        views.resize,
        name="imagefit_resize"),
]

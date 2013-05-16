from django.conf.urls import url, patterns


urlpatterns = patterns(
    '',
    url(
        r'^(?P<path_name>[\w_-]*)/(?P<format>[,\w-]+)/(?P<url>.*)/?$',
        'imagefit.views.resize',
        name="imagefit_resize"),
)

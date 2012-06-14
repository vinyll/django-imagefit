from django.conf.urls.shortcut import urlpatterns
from django.conf.urls import url, include, patterns

urlpatterns = patterns('',
    url(r'^resize/(?P<format>[\w-]+)/(?P<url>.*)$', 'imagefit.views.resize', name="imagefit_resize"),
)

from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^resize/(?P<format>[\w-]+)/(?P<url>.*)$', 'imagefit.views.resize', name="imagefit_resize"),
)

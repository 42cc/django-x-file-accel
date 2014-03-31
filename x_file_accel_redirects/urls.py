from django.conf.urls.defaults import patterns, url

from x_file_accel_redirects import views

urlpatterns = patterns('',
    url(r'^(?P<prefix>[^/]+)/(?P<filepath>.+)$', views.accel_view, name='accel_view'),
    url(r'^(?P<prefix>[^/]+)$', views.accel_view, name='accel_view_root'),
)

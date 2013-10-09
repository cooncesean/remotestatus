from django.conf.urls import patterns, include, url

urlpatterns = patterns('remotestatus.views',
    url(r'^box/(?P<box_id>[0-9]+)/$', 'box_detail', name='remotestatus-box-detail'),
    url(r'^$', 'dashboard', name='remotestatus-dashboard'),
)
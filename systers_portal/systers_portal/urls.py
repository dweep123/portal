from django.conf.urls import patterns, include, url
from django.contrib import admin

try:
    from systers_portal import settings
except ImportError:
    from systers_portal.systers_portal import settings

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    pass

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/(?P<username>[\w.@+-]+)/$',
        'dashboard.views.view_userprofile',
        name='view_userprofile'),
    url(r'^users/(?P<username>[\w.@+-]+)/edit/$',
        'dashboard.views.edit_userprofile', name='edit_userprofile'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/(?P<page_slug>[a-zA-Z0-9_-]+)'
        r'/edit/$', 'dashboard.views.edit_page', name='edit_page'),

    url(r'^$', 'dashboard.views.index', name='index',),
    url(r'^', include('cms.urls')),
)

urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
     'serve',
     {'document_root': settings.base.MEDIA_ROOT}), )

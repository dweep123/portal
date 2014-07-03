from django.conf.urls import patterns, include, url
from django.contrib import admin
from systers_portal import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^resource_area/', include('resource_area.urls')),
    url(r'^', include('dashboard.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^cms/', include('cms.urls')),
    url(r'^superadmin_dashboard/',
       include('superadmin_dashboard.urls')),
)
urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
     'serve',
     {'document_root': settings.base.MEDIA_ROOT}), )

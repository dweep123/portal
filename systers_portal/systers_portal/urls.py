from django.conf.urls import patterns, include, url
from django.contrib import admin

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    pass

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/$',
        'dashboard.views.view_news', name='view_news'),
    url(r'^', include('cms.urls')),
)

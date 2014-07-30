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
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/$',
        'dashboard.views.community_main_page',
        name='community_main_page'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/profile/$',
        'dashboard.views.view_community_profile',
        name='view_community_profile'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/manage_pages/$',
        'dashboard.views.manage_pages',
        name='manage_pages'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/edit/$',
        'dashboard.views.edit_community_profile',
        name='edit_community_profile'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/$',
        'dashboard.views.show_community_news', name='show_community_news'),
    url('^(?P<community_slug>[a-zA-Z0-9_-]+)/news/add/',
        'dashboard.views.add_news', name='add_news'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/$',
        'dashboard.views.view_news', name='view_news'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/add_comment$',
        'dashboard.views.add_newscomment', name='add_newscomment'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/delete_comment$',
        'dashboard.views.delete_newscomment', name='delete_newscomment'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/delete_comment/(?P<comment_id>\d+)/$',
        'dashboard.views.delete_newscomment', name='delete_newscomment'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/edit/$',
        'dashboard.views.edit_news', name='edit_news'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/delete/$',
        'dashboard.views.delete_news', name='delete_news'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/confirm_delete/$',
        'dashboard.views.confirm_delete_news', name='confirm_delete_news'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/add/',
        'dashboard.views.add_resource', name='add_resource'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/'
        r'(?P<resource_slug>[a-zA-Z0-9_-]+)/delete_comment$',
        'dashboard.views.delete_resourcecomment',
        name='delete_resourcecomment'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/'
        r'(?P<resource_slug>[a-zA-Z0-9_-]+)/'
        r'delete_comment/(?P<comment_id>\d+)/$',
        'dashboard.views.delete_resourcecomment',
        name='delete_resourcecomment'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/'
        r'(?P<resource_slug>[a-zA-Z0-9_-]+)/delete/$',
        'dashboard.views.delete_resource', name='delete_resource'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/'
        r'(?P<resource_slug>[a-zA-Z0-9_-]+)/confirm_delete/$',
        'dashboard.views.confirm_delete_resource',
        name='confirm_delete_resource'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/'
        r'(?P<resource_slug>[a-zA-Z0-9_-]+)/edit/$',
        'dashboard.views.edit_resource', name='edit_resource'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/'
        r'(?P<resource_slug>[a-zA-Z0-9_-]+)/$',
        'dashboard.views.view_resource', name='view_resource'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/'
        r'(?P<resource_slug>[a-zA-Z0-9_-]+)/add_comment$',
        'dashboard.views.add_resourcecomment', name='add_resourcecomment'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/resources/',
        'dashboard.views.show_community_resources',
        name='show_community_resources'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/(?P<page_slug>[a-zA-Z0-9_-]+)/$',
        'dashboard.views.view_page', name='view_page'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/(?P<page_slug>[a-zA-Z0-9_-]+)'
        r'/edit/$', 'dashboard.views.edit_page', name='edit_page'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/(?P<page_slug>[a-zA-Z0-9_-]+)'
        r'/delete/$', 'dashboard.views.delete_page', name='delete_page'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/(?P<page_slug>[a-zA-Z0-9_-]+)'
        r'/confirm_delete/$', 'dashboard.views.confirm_delete_page',
        name='confirm_delete_page'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/delete/$',
        'dashboard.views.delete_news', name='delete_news'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/news/'
        r'(?P<news_slug>[a-zA-Z0-9_-]+)/confirm_delete/$',
        'dashboard.views.confirm_delete_news', name='confirm_delete_news'),
    url(r'^(?P<community_slug>[a-zA-Z0-9_-]+)/page/add/$',
        'dashboard.views.add_page', name='add_page'),
    url(r'^$', 'dashboard.views.index', name='index',),
    url(r'^', include('cms.urls')),
)

urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
     'serve',
     {'document_root': settings.base.MEDIA_ROOT}), )

from django.conf.urls import patterns, url
from resource_area import views
urlpatterns = patterns('',
                       url(r'^(?P<community_name_url>\w+)$',
                           views.community_resourcearea, name='community_resourcearea'),
                       url(r'^edit_profile/(?P<community_name_url>\w+)$',
                           views.community_editprofile, name='community_profile'),
                       url(r'^News/(?P<community_name_url>\w+)$',
                           views.community_News, name='community_news'),
                       url(r'^add_news/(?P<community_name_url>\w+)$',
                           views.add_news, name='add_news'),
                       url(r'^view_news/(?P<news_id>\w+)$',
                           views.view_news, name='view_news'),
                       url(r'^edit_news/(?P<news_id>\w+)$',
                           views.edit_news, name='edit_news'),
                       url(r'^delete_news/(?P<news_id>\w+)$',
                           views.delete_news, name='delete_news'),
                       url(r'^sure_delete_news/(?P<news_id>\w+)$',
                           views.sure_delete_news, name='sure_delete_news'),
                       url(r'^add_page/(?P<community_name_url>\w+)$',
                           views.add_page, name='add_page'),
                       )
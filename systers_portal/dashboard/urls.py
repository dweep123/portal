from django.conf.urls import patterns
from django.conf.urls import url
from dashboard import views
urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'index/$', views.index, name='index'),
                       url(r'^view_profile/(?P<user_name_url>\w+)/$',
                           views.view_profile, name='profiles'),
                       url(r'^edit_profile/$', views.edit_profile,
                           name='editprofile'),
                       )

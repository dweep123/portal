from django.conf.urls import patterns,url
from dashboard import views
urlpatterns = patterns('',
		url(r'^$',views.index,name='index'),
		url(r'^profile/(?P<user_name_url>\w+)/$', views.profiles, name='profiles'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^edit_profile/$', views.edit_profile, name='editprofile'),
		url(r'^change_password/$', views.change_password, name='changeprofile'),
		)

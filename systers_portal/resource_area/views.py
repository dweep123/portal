from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from dashboard.models import SysterUser, Community, News, Resource, CommunityPage
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from resource_area.forms import CommunityForm
from resource_area.forms import NewsAddForm
from resource_area.forms import NewsEditForm
from resource_area.forms import PageAddForm
from cms.models.pagemodel import Page
from cms.api import create_page


def community_resourcearea(request, community_name_url):
    context = RequestContext(request)
    community_name = community_name_url.replace('_', ' ')
    context_dic = {'community_name': community_name}
    context_dic['community_name_url'] = community_name_url
    try:
        community = Community.objects.get(name=community_name)
        context_dic["community"] = community
        community.url = community_name_url
	pages =  CommunityPage.objects.filter(community=community)
	for page in pages:
		page.url = page.title.lower()+"_"+page.community.name.replace(' ','_').lower()
	context_dic['pages']=pages
    except Community.DoesNotExist:
        pass
    return render_to_response('resource_area/edit_resource_area.html', context_dic, context)


def community_editprofile(request, community_name_url):
    context = RequestContext(request)
    community_name = community_name_url.replace('_', ' ')
    context_dic = {'community_name': community_name}
    context_dic['community_name_url'] = community_name_url
    try:
        community = Community.objects.get(name=community_name)
        context_dic["community"] = community
        if request.method == 'POST':
            communityform = CommunityForm(
                data=request.POST, instance=community)
            context_dic['communityform'] = communityform
            if communityform.is_valid():
                community = communityform.save()
                return community_resourcearea(request, community_name_url)
            else:
                print communityform.errors
        else:
            communityform = CommunityForm(instance=community)
            context_dic['communityform'] = communityform

    except Community.DoesNotExist:
        pass

    return render_to_response('resource_area/edit_communityprofile.html', context_dic, context)


def community_News(request, community_name_url):
    context = RequestContext(request)
    community_name = community_name_url.replace('_', ' ')
    context_dic = {'community_name': community_name}
    context_dic['community_name_url'] = community_name_url
    try:
        community = Community.objects.get(name=community_name)
        context_dic["community"] = community
        news_list = News.objects.filter(community=community)
        context_dic['news_list'] = news_list
    except Community.DoesNotExist:
        pass
    return render_to_response('resource_area/show_news.html', context_dic, context)


def add_news(request, community_name_url):
    context = RequestContext(request)
    community_name = community_name_url.replace('_', ' ')
    context_dic = {'community_name': community_name}
    context_dic['community_name_url'] = community_name_url
    try:
	 community = Community.objects.get(name=community_name)
   	 if request.method == 'POST':
              form = NewsAddForm(request.POST)
  	      if form.is_valid():
		    news = form.save(commit=False)
	    	    news.community = community
	    	    news.author = SysterUser.objects.get(user=request.user)
     	            news.save()
		    return community_News(request, community_name_url)
  	      else:
        	    print form.errors
    	 else:
        	form = NewsAddForm()
		context_dic['form']=form
    
    except Community.DoesNotExist:
        pass
    return render_to_response('resource_area/add_news.html', context_dic,context)



def view_news(request, news_id):
    context = RequestContext(request)
    context_dic = {'news_id': news_id}
    try:
        news = News.objects.get(id=news_id)
        context_dic["news"] = news
    except News.DoesNotExist:
        pass
    return render_to_response('resource_area/view_news.html', context_dic, context)


def edit_news(request, news_id):
    context = RequestContext(request)
    context_dic = {'news_id': news_id}
    try:
      	news = News.objects.get(id=news_id)
        context_dic["news"] = news
        if request.method == 'POST':
            newsform = NewsEditForm(
                data=request.POST, instance=news)
            context_dic['newsform'] = newsform
            if newsform.is_valid():
                news = newsform.save()
                return view_news(request, news_id)
            else:
                print newsform.errors
        else:
            newsform = NewsEditForm(instance=news)
            context_dic['newsform'] = newsform

    except News.DoesNotExist:
        pass

    return render_to_response('resource_area/edit_news.html', context_dic, context)


def delete_news(request, news_id):
    context = RequestContext(request)
    context_dic = {'news_id': news_id}
    return render_to_response('resource_area/delete_news.html', context_dic, context)


def sure_delete_news(request, news_id):
    context = RequestContext(request)
    context_dic = {'news_id': news_id}
    try:
        news = News.objects.get(id=news_id)
	community = news.community.name.replace("  ","_")
	news.delete()
	return community_News(request,community)
    except News.DoesNotExist:
    	return render_to_response('resource_area/error_delete_news.html', context_dic, context)


def add_page(request, community_name_url):
    context = RequestContext(request)
    community_name = community_name_url.replace('_', ' ')
    context_dic = {'community_name': community_name}
    context_dic['community_name_url'] = community_name_url
    try:
	 community = Community.objects.get(name=community_name)
   	 if request.method == 'POST':
              form = PageAddForm(request.POST)
  	      if form.is_valid():
		    community_page = form.save(commit=False)
	    	    community_page.community = community
		    cms_page = create_page(community_page.title+"_"+community_name_url,'page_template.html','en-us')
		    community_page.page=cms_page
     	            community_page.save()
		    return community_resourcearea(request, community_name_url)
  	      else:
        	    print form.errors
    	 else:
        	form = PageAddForm()
		context_dic['form']=form
    
    except Community.DoesNotExist:
        pass
    return render_to_response('resource_area/add_page.html', context_dic,context)

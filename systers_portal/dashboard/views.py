from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from guardian.decorators import permission_required_or_403

from dashboard.forms import (UserForm, CommunityForm, NewsForm,
                             ResourceForm, PageForm, UserGroupsForm,
                             NewsCommentForm, ResourceCommentForm)
from dashboard.models import (CommunityPage, Community, SysterUser, News,
                              Resource, NewsComment, ResourceComment)


class ExtraContextTemplateView(TemplateView):
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super(ExtraContextTemplateView, self).get_context_data(*args,
                                                                         **kwargs)
        if self.extra_context:
            context.update(self.extra_context)
        return context


@login_required
@permission_required_or_403('dashboard.change_community_page',
                            (Community, 'slug', 'community_slug'))
def edit_page(request, community_slug, page_slug):
    """Edit page in a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param page_slug: string page_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
                     or page for that community does not exist
    """
    community = get_object_or_404(Community, slug=community_slug)
    page = get_object_or_404(
        CommunityPage, community=community, slug=page_slug)
    return render_to_response('page_template.html', {'page': page},
                              context_instance=RequestContext(request))


def view_page(request, community_slug, page_slug):
    """View page in a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param page_slug: string page_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
                     or page for that community does not exist
    """
    community = get_object_or_404(Community, slug=community_slug)
    page = get_object_or_404(
        CommunityPage, community=community, slug=page_slug)
    Pages = CommunityPage.objects.filter(community=community)
    return render_to_response('dashboard/view_page.html',
                              {'community': community, 'page': page,
                               'Pages': Pages, 'active_page': page.slug},
                              context_instance=RequestContext(request))


@login_required
@permission_required_or_403('dashboard.change_community_page',
                            (Community, 'slug', 'community_slug'))
def manage_pages(request, community_slug):
    """Manage Pages in a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    Pages = CommunityPage.objects.filter(community=community)
    return render_to_response('dashboard/manage_pages.html',
                              {'Pages': Pages, 'community': community},
                              context)


@login_required
@permission_required_or_403('dashboard.add_community_page',
                            (Community, 'slug__exact', 'community_slug'))
def add_page(request, community_slug):
    """Add page for a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.community = community
            page.save()
            return redirect('edit_page',
                            community_slug=community.slug,
                            page_slug=page.slug)
    else:
        form = PageForm()
    return render_to_response('dashboard/add_page.html',
                              {'form': form, 'community': community},
                              context)


@login_required
@permission_required_or_403('dashboard.delete_community_page',
                            (Community, 'slug__exact', 'community_slug'))
def delete_page(request, community_slug, page_slug):
    """Ask Confirmation to delete page of a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param page_slug: string page_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    page = get_object_or_404(
        CommunityPage, community=community, slug=page_slug)
    return render_to_response('dashboard/delete_page.html',
                              {'page': page},
                              context)


@login_required
@permission_required_or_403('dashboard.delete_community_page',
                            (Community, 'slug__exact', 'community_slug'))
def confirm_delete_page(request, community_slug, page_slug):
    """Delete page of a community after confirmation

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param page_slug: string page_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    community = get_object_or_404(Community, slug=community_slug)
    page = get_object_or_404(
        CommunityPage, community=community, slug=page_slug)
    page.delete()
    return redirect('manage_pages', community_slug=community.slug)


def community_main_page(request, community_slug):
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    Pages = CommunityPage.objects.filter(community=community)
    return render_to_response('dashboard/community_main_page.html',
                              {'community': community, 'Pages': Pages,
                               'active_page': 'home'},
                              context)


def view_user_profile(request, username):
    """View profile of a user

    :param request: request object
    :param username: string username parsed from the URL
    :raises Http404: if a user entry doesn't exist
    """
    context = RequestContext(request)
    user = get_object_or_404(User, username=username)
    systeruser = SysterUser.objects.get(user=user)
    return render_to_response('dashboard/view_profile.html',
                              {'systeruser': systeruser},
                              context)


@login_required
def edit_user_profile(request, username):
    context = RequestContext(request)
    if request.method == 'POST':
        userform = UserForm(data=request.POST, instance=request.user)
        if userform.is_valid():
            user = userform.save()
            systeruser = user.systeruser
            if 'profile_picture' in request.FILES:
                systeruser.profile_picture = request.FILES['profile_picture']
            systeruser.save()
            return HttpResponseRedirect(
                reverse('view_userprofile', args=(user.username,)))
    else:
        userform = UserForm(instance=request.user)
    return render_to_response(
        'accounts/edit_user_profile.html',
        {'userform': userform},
        context)


def view_community_profile(request, community_slug):
    """Display profile of a community

    :param request: request object
    :param community_slug: string slug parsed from the URL
    """
    community = get_object_or_404(Community, slug=community_slug)
    return render_to_response('dashboard/view_community_profile.html',
                              {'community': community})


@login_required
@permission_required_or_403('dashboard.change_community',
                            (Community, 'slug__exact', 'community_slug'))
def edit_community_profile(request, community_slug):
    """Edit profile of a community

    :param request: request object
    :param community_slug: string slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    :raises Http403: if user has no permissions to edit the community profile
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return redirect('view_community_profile',
                            community_slug=community.slug)
        community = get_object_or_404(Community, slug=community_slug)
    else:
        form = CommunityForm(instance=community)
    return render_to_response('dashboard/edit_community_profile.html',
                              {'form': form, 'community': community}, context)


def view_news(request, community_slug, news_slug):
    """View a particluar news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community entry or news entry
                     inside that community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    comments = NewsComment.objects.filter(news=news)
    form = NewsCommentForm()
    Pages = CommunityPage.objects.filter(community=community)
    return render_to_response('dashboard/view_news.html',
                              {'news': news, 'comments':
                               comments, 'form': form, 'active_page': 'news', 'Pages': Pages},
                              context)


@login_required
def add_newscomment(request, community_slug, news_slug):
    """Add a new comment."""
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    if request.method == 'POST':
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.author = SysterUser.objects.get(user=request.user)
            comment.save()
            return redirect('view_news',
                            community_slug=community.slug,
                            news_slug=news.slug)
    else:
        form = NewsCommentForm()
    return redirect('view_news',
                    community_slug=community.slug,
                    news_slug=news.slug)


@login_required
def delete_newscomment(request, community_slug, news_slug, comment_id=None):
    """Delete comment(s) with primary key
    comment_id or with comment_ids in POST."""
    community = get_object_or_404(Community, slug=community_slug)
    if not comment_id:
        commentlist = request.POST.getlist("delete")
    else:
        commentlist = [comment_id]
    for comment_id in commentlist:
        NewsComment.objects.get(pk=comment_id).delete()
    return redirect('view_news',
                    community_slug=community.slug,
                    news_slug=news_slug)


def show_community_news(request, community_slug):
    """Show all news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = News.objects.filter(community=community)
    Pages = CommunityPage.objects.filter(community=community)
    return render_to_response('dashboard/show_community_news.html',
                              {'News': news, 'community': community, 'active_page': 'news', 'Pages': Pages}, context)


@login_required
@permission_required_or_403('dashboard.add_community_news',
                            (Community, 'slug__exact', 'community_slug'))
def add_news(request, community_slug):
    """Add news for a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.community = community
            news.author = SysterUser.objects.get(user=request.user)
            news.save()
            return redirect('show_community_news',
                            community_slug=community.slug)
    else:
        form = NewsForm()
    return render_to_response('dashboard/add_news.html',
                              {'form': form, 'community': community},
                              context)


@login_required
@permission_required_or_403('dashboard.change_community_news',
                            (Community, 'slug__exact', 'community_slug'))
def edit_news(request, community_slug, news_slug):
    """Edit a particluar news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community entry or news entry
    inside that community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    if request.method == 'POST':
        newsform = NewsForm(request.POST, instance=news)
        if newsform.is_valid():
            changed_news = newsform.save()
            return redirect('view_news',
                            community_slug=community.slug,
                            news_slug=changed_news.slug)
        news = get_object_or_404(News, community=community, slug=news_slug)
    else:
        newsform = NewsForm(instance=news)
    return render_to_response('dashboard/edit_news.html',
                              {'newsform': newsform, 'news': news},
                              context)


@login_required
@permission_required_or_403('dashboard.delete_community_news',
                            (Community, 'slug__exact', 'community_slug'))
def delete_news(request, community_slug, news_slug):
    """Ask Confirmation to delete news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    return render_to_response('dashboard/delete_news.html',
                              {'news': news},
                              context)


@login_required
@permission_required_or_403('dashboard.delete_community_news',
                            (Community, 'slug__exact', 'community_slug'))
def confirm_delete_news(request, community_slug, news_slug):
    """Delete news about a community after confirmation

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param news_slug: string news_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    community = get_object_or_404(Community, slug=community_slug)
    news = get_object_or_404(News, community=community, slug=news_slug)
    news.delete()
    return redirect('show_community_news', community_slug=community.slug)


def view_resource(request, community_slug, resource_slug):
    """View a particluar resource of a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param resource_slug: string resource_slug parsed from the URL
    :raises Http404: if a community entry or resource entry
                     inside that community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    resource = get_object_or_404(Resource,
                                 community=community,
                                 slug=resource_slug)
    comments = ResourceComment.objects.filter(resource=resource)
    form = ResourceCommentForm()
    return render_to_response('dashboard/view_resource.html',
                              {'resource': resource,
                               'comments': comments,
                               'form': form},
                              context)


def show_community_resources(request, community_slug):
    """Show all resources of a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    resources = Resource.objects.filter(community=community)
    Pages = CommunityPage.objects.filter(community=community)
    return render_to_response('dashboard/show_community_resources.html',
                              {'Resources': resources, 'community': community,
                               'active_page': 'resources', 'Pages': Pages},
                              context)


@login_required
def add_resourcecomment(request, community_slug, resource_slug):
    """Add a resource comment."""
    community = get_object_or_404(Community, slug=community_slug)
    resource = get_object_or_404(
        Resource, community=community, slug=resource_slug)
    if request.method == 'POST':
        form = ResourceCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.author = SysterUser.objects.get(user=request.user)
            comment.save()
            return redirect('view_resource',
                            community_slug=community.slug,
                            resource_slug=resource.slug)
    else:
        form = ResourceCommentForm()
    return redirect('view_resource',
                    community_slug=community.slug,
                    resource_slug=resource.slug)


@login_required
def delete_resourcecomment(request, community_slug,
                           resource_slug, comment_id=None):
    """Delete comment(s) with primary key
    comment_id or with comment_ids in POST."""
    community = get_object_or_404(Community, slug=community_slug)
    if not comment_id:
        commentlist = request.POST.getlist("delete")
    else:
        commentlist = [comment_id]
    for comment_id in commentlist:
        ResourceComment.objects.get(pk=comment_id).delete()
    return redirect('view_resource',
                    community_slug=community.slug,
                    resource_slug=resource_slug)


@login_required
@permission_required_or_403('dashboard.add_community_resource',
                            (Community, 'slug__exact', 'community_slug'))
def add_resource(request, community_slug):
    """Add resource for a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.community = community
            resource.author = SysterUser.objects.get(user=request.user)
            resource.save()
            return redirect('show_community_resources',
                            community_slug=community.slug)
    else:
        form = ResourceForm()
    return render_to_response('dashboard/add_resource.html',
                              {'form': form, 'community': community},
                              context)


@login_required
@permission_required_or_403('dashboard.change_community_resource',
                            (Community, 'slug__exact', 'community_slug'))
def edit_resource(request, community_slug, resource_slug):
    """Edit a particular resource of a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param resource_slug: string resource_slug parsed from the URL
    :raises Http404: if a community entry or resource entry
                     inside that community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    resource = get_object_or_404(Resource,
                                 community=community,
                                 slug=resource_slug)
    if request.method == 'POST':
        resourceform = ResourceForm(request.POST, instance=resource)
        if resourceform.is_valid():
            changed_resource = resourceform.save()
            return redirect('view_resource',
                            community_slug=community.slug,
                            resource_slug=changed_resource.slug)
        resource = get_object_or_404(Resource,
                                     community=community,
                                     slug=resource_slug)
    else:
        resourceform = ResourceForm(instance=resource)
    return render_to_response('dashboard/edit_resource.html',
                              {'resourceform': resourceform,
                               'resource': resource},
                              context)


@login_required
@permission_required_or_403('dashboard.delete_community_resource',
                            (Community, 'slug__exact', 'community_slug'))
def delete_resource(request, community_slug, resource_slug):
    """Ask Confirmation to delete resource of a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param resource_slug: string resource_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    resource = get_object_or_404(
        Resource, community=community, slug=resource_slug)
    return render_to_response('dashboard/delete_resource.html',
                              {'resource': resource},
                              context)


@login_required
@permission_required_or_403('dashboard.delete_community_resource',
                            (Community, 'slug__exact', 'community_slug'))
def confirm_delete_resource(request, community_slug, resource_slug):
    """Delete resource of a community after confirmation

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :param resource_slug: string resource_slug parsed from the URL
    :raises Http404: if a community or news entry
                     inside community doesn't exist
    """
    community = get_object_or_404(Community, slug=community_slug)
    resource = get_object_or_404(
        Resource, community=community, slug=resource_slug)
    resource.delete()
    return redirect('show_community_resources', community_slug=community.slug)


@login_required
@permission_required_or_403('dashboard.change_community_systeruser',
                            (Community, 'slug__exact', 'community_slug'))
def manage_community_users(request, community_slug):
    """Manage all community users

    :param request:
    :param community_slug:
    :return:
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    users = community.members.all()
    return render_to_response('dashboard/community_users.html',
                              {'community': community, 'users': users}, context)


@login_required
@permission_required_or_403('dashboard.change_community_systeruser',
                            (Community, 'slug__exact', 'community_slug'))
def manage_user_groups(request, community_slug, username):
    """Manage the auth groups of a user

    :param community_slug: string community_slug parsed from the URL
    :param username: string username parsed from the URL
    """
    context = RequestContext(request)
    user = get_object_or_404(User, username=username)
    community = get_object_or_404(Community, slug=community_slug)
    if request.method == 'POST':
        form = UserGroupsForm(request.POST, community_name=community.name, username=username)
        if form.is_valid():
            form.save(community=community, user=user)
            return redirect('manage_community_users',
                            community_slug=community.slug)
    else:
        form = UserGroupsForm(community_name=community.name, username=username)
    return render_to_response('dashboard/user_groups.html',
                              {'form': form, 'user': user, 'community': community}, context)

@login_required
def community_proposal(request):
    """Render google form for new community requests"""
    return render_to_response('dashboard/community_proposal.html')

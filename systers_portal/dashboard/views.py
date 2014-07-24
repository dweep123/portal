from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from guardian.decorators import permission_required_or_403

from dashboard.forms import UserForm, CommunityForm
from dashboard.models import CommunityPage, Community, SysterUser, News


@login_required
@permission_required_or_403('dashboard.change_community_page',
                            (Community, 'slug', 'community_slug'))
def edit_page(request, community_slug, page_slug):
    page = get_object_or_404(CommunityPage, slug=page_slug)
    return render_to_response('page_template.html', {'page': page},
                              context_instance=RequestContext(request))


def index(request):
    context = RequestContext(request)
    return render_to_response('dashboard/index.html', {}, context)


def view_userprofile(request, username):
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
def edit_userprofile(request, username):
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
        'dashboard/edit_profile.html',
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
    return render_to_response('dashboard/view_news.html',
                              {'news': news}, context)


def show_community_news(request, community_slug):
    """Show all news about a community

    :param request: request object
    :param community_slug: string community_slug parsed from the URL
    :raises Http404: if a community entry doesn't exist
    """
    context = RequestContext(request)
    community = get_object_or_404(Community, slug=community_slug)
    news = News.objects.filter(community=community)
    return render_to_response('dashboard/show_community_news.html',
                              {'News': news},
                              context)

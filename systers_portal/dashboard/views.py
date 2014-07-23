from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from guardian.decorators import permission_required_or_403

from dashboard.decorators import authorship_required
from dashboard.forms import UserForm
from dashboard.models import CommunityPage, Community, SysterUser


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

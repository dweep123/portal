from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from dashboard.models import SysterUser
from dashboard.forms import SysterUserForm
from dashboard.forms import UserForm


def index(request):
    context = RequestContext(request)
    return render_to_response('dashboard/index.html', {}, context)


def view_profile(request, user_name_url):
    context = RequestContext(request)
    user_name = user_name_url
    context_dic = {'user_name': user_name}
    try:
        user = User.objects.get(username=user_name)
        systeruser = SysterUser.objects.get(user=user)
        context_dic['user'] = user
        context_dic['systeruser'] = systeruser
    except User.DoesNotExist:
        pass
    return render_to_response('dashboard/view_profile.html',
                              context_dic, context)


@login_required
def edit_profile(request):
    context = RequestContext(request)
    if request.method == 'POST':
        userform = UserForm(data=request.POST, instance=request.user)
        systeruserform = SysterUserForm(data=request.POST,
                                        instance=SysterUser.objects.get(user=request.user))
        if userform.is_valid() and systeruserform.is_valid():
            user = userform.save()
            systeruser = systeruserform.save(commit=False)
            if 'profile_picture' in request.FILES:
                systeruser.profile_picture = request.FILES['profile_picture']
            systeruser.save()
            return HttpResponseRedirect('/dashboard/view_profile/' + user.username + '/')

        else:
            print userform.errors, systeruserform.errors
    else:
        userform = UserForm(instance=request.user)
        systeruserform = SysterUserForm(
            instance=SysterUser.objects.get(user=request.user))
    return render_to_response('dashboard/edit_profile.html',
                              {'userform': userform, 'systeruserform': systeruserform},
                              context)
